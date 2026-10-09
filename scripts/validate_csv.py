#!/usr/bin/env python3
"""Validate RadioSync CSV files using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "frequency-record.schema.json"
DEFAULT_DATA_ROOT = REPO_ROOT / "dados"
DATE_FIELDS = (
    "source_publication_date",
    "source_accessed_date",
    "last_independently_verified_date",
)
FREQUENCY_FIELDS = ("rx_frequency_mhz", "tx_frequency_mhz")


@dataclass(frozen=True)
class Finding:
    level: str
    path: Path
    row: int | None
    message: str

    def __str__(self) -> str:
        location = str(self.path)
        if self.row is not None:
            location += f":{self.row}"
        return f"{self.level}: {location}: {self.message}"


def load_schema(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    if not schema.get("x-csv-columns") or not schema.get("properties"):
        raise ValueError(f"Schema {path} lacks CSV metadata")
    columns = schema["x-csv-columns"]
    properties = schema["properties"]
    if len(columns) != len(set(columns)):
        raise ValueError(f"Schema {path} contains duplicate CSV columns")
    if set(columns) != set(properties):
        raise ValueError(f"Schema {path} columns and properties do not match")
    if not set(schema.get("required", ())).issubset(properties):
        raise ValueError(f"Schema {path} requires undefined properties")
    return schema


def iter_csv_files(root: Path) -> Iterable[Path]:
    return sorted(path for path in root.rglob("*.csv") if path.is_file())


def _valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _property_error(name: str, value: str, definition: dict) -> str | None:
    if "enum" in definition and value not in definition["enum"]:
        return f"{name} has unsupported value {value!r}"
    pattern = definition.get("pattern")
    if pattern and re.fullmatch(pattern, value) is None:
        return f"{name} has invalid format {value!r}"
    minimum = definition.get("minLength")
    if minimum is not None and len(value) < minimum:
        return f"{name} must not be empty"
    return None


def _validate_cross_fields(row: dict[str, str]) -> list[str]:
    errors: list[str] = []

    for field in DATE_FIELDS:
        value = row[field]
        if value and not _valid_date(value):
            errors.append(f"{field} is not a valid ISO date")
        elif value and date.fromisoformat(value) > date.today():
            errors.append(f"{field} must not be in the future")

    publication_date = row["source_publication_date"]
    accessed_date = row["source_accessed_date"]
    if publication_date and accessed_date and _valid_date(publication_date) and _valid_date(accessed_date):
        if date.fromisoformat(publication_date) > date.fromisoformat(accessed_date):
            errors.append("source_publication_date must not be later than source_accessed_date")

    for field in FREQUENCY_FIELDS:
        value = row[field]
        if not value:
            continue
        try:
            number = float(value)
        except ValueError:
            errors.append(f"{field} must be numeric")
            continue
        if not math.isfinite(number) or not 0 < number <= 1_000_000:
            errors.append(f"{field} must be greater than zero and at most 1,000,000 MHz")

    latitude = row["latitude"]
    longitude = row["longitude"]
    if bool(latitude) != bool(longitude):
        errors.append("latitude and longitude must be supplied together")
    if latitude and longitude:
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                errors.append("latitude or longitude is outside its valid range")
        except ValueError:
            errors.append("latitude and longitude must be decimal numbers")
        if not row["location_precision"]:
            errors.append("location_precision is required when coordinates are present")

    if row["municipality_name"]:
        if not row["municipality_id"] or not row["municipality_slug"]:
            errors.append("municipality_id and municipality_slug are required for municipal records")
    elif row["municipality_id"] or row["municipality_slug"]:
        errors.append("municipality_name is required when a municipality identifier is present")

    if row["country_code"] == "BR":
        if row["state_id"] and not re.fullmatch(r"[0-9]{2}", row["state_id"]):
            errors.append("Brazilian state_id must be the two-digit IBGE UF code")
        if row["municipality_id"] and not re.fullmatch(r"[0-9]{7}", row["municipality_id"]):
            errors.append("Brazilian municipality_id must be a seven-digit IBGE code")

    parsed = urlparse(row["source_url"])
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append("source_url must be an absolute HTTPS URL")

    if row["source_type"] == "independent_reception":
        if not row["last_independently_verified_date"] or not row["verification_method"]:
            errors.append("independent reception requires a verification date and method")
        if row["verification_status"] != "independently_verified":
            errors.append("independent reception must use independently_verified status")

    if row["verification_status"] == "independently_verified" and not row["last_independently_verified_date"]:
        errors.append("independently_verified status requires last_independently_verified_date")

    if row["verification_status"] == "independently_verified" and not row["verification_method"]:
        errors.append("independently_verified status requires verification_method")

    if row["operational_status"].startswith("verified_") and row["verification_status"] != "independently_verified":
        errors.append("verified operational status requires independent verification")

    if row["redistribution_permission"] in {"allowed", "allowed_with_attribution"}:
        if not row["data_license"]:
            errors.append("redistributable records require data_license")
        if not row["attribution"]:
            errors.append("redistributable records require attribution")

    return errors


def validate_file(path: Path, schema: dict) -> tuple[list[Finding], list[dict[str, str]]]:
    findings: list[Finding] = []
    rows: list[dict[str, str]] = []
    expected = schema["x-csv-columns"]
    required = set(schema["required"])

    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected:
                missing = [name for name in expected if name not in (reader.fieldnames or [])]
                extra = [name for name in (reader.fieldnames or []) if name not in expected]
                detail = []
                if missing:
                    detail.append("missing columns: " + ", ".join(missing))
                if extra:
                    detail.append("unexpected columns: " + ", ".join(extra))
                if not missing and not extra:
                    detail.append("columns are not in canonical order")
                findings.append(Finding("ERROR", path, 1, "; ".join(detail)))
                return findings, rows

            for line_number, raw_row in enumerate(reader, start=2):
                if None in raw_row:
                    extra_values = raw_row.pop(None) or []
                    findings.append(
                        Finding(
                            "ERROR",
                            path,
                            line_number,
                            f"row has {len(extra_values)} value(s) beyond the canonical columns",
                        )
                    )
                row = {key: (value or "").strip() for key, value in raw_row.items()}
                rows.append(row)
                for field in required:
                    if not row[field]:
                        findings.append(Finding("ERROR", path, line_number, f"{field} is required"))
                for field, definition in schema["properties"].items():
                    message = _property_error(field, row[field], definition)
                    if message:
                        findings.append(Finding("ERROR", path, line_number, message))
                for message in _validate_cross_fields(row):
                    findings.append(Finding("ERROR", path, line_number, message))
    except (OSError, UnicodeError, csv.Error) as exc:
        findings.append(Finding("ERROR", path, None, f"cannot read CSV: {exc}"))

    return findings, rows


def validate_tree(root: Path, schema_path: Path = DEFAULT_SCHEMA) -> list[Finding]:
    schema = load_schema(schema_path)
    findings: list[Finding] = []
    all_rows: list[tuple[Path, int, dict[str, str]]] = []
    files = list(iter_csv_files(root))
    if not files:
        return [Finding("ERROR", root, None, "no CSV files found")]

    for path in files:
        file_findings, rows = validate_file(path, schema)
        findings.extend(file_findings)
        all_rows.extend((path, index, row) for index, row in enumerate(rows, start=2))

    ids: dict[str, tuple[Path, int]] = {}
    technical_keys: dict[tuple[str, ...], tuple[Path, int]] = {}
    for path, line, row in all_rows:
        record_id = row["record_id"]
        if record_id in ids:
            first_path, first_line = ids[record_id]
            findings.append(Finding("ERROR", path, line, f"duplicate record_id; first seen at {first_path}:{first_line}"))
        else:
            ids[record_id] = (path, line)

        key = tuple(
            row[name]
            for name in (
                "country_code", "state_code", "municipality_id", "locality_id", "service",
                "callsign", "channel_designator", "rx_frequency_mhz", "tx_frequency_mhz",
            )
        )
        if key in technical_keys:
            first_path, first_line = technical_keys[key]
            findings.append(Finding("ERROR", path, line, f"duplicate technical record; first seen at {first_path}:{first_line}"))
        else:
            technical_keys[key] = (path, line)

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_DATA_ROOT, help="directory containing CSV files")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="schema JSON path")
    args = parser.parse_args(argv)

    findings = validate_tree(args.root.resolve(), args.schema.resolve())
    for finding in findings:
        print(finding)
    errors = sum(finding.level == "ERROR" for finding in findings)
    files = len(list(iter_csv_files(args.root.resolve())))
    if errors:
        print(f"Validation failed: {errors} error(s) across {files} CSV file(s).")
        return 1
    print(f"Validation passed: {files} CSV file(s), no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
