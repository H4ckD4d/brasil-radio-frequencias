from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_csv import DEFAULT_MUNICIPALITY_SCHEMA, DEFAULT_SCHEMA, load_schema, validate_tree


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_schema(DEFAULT_SCHEMA)
        cls.columns = cls.schema["x-csv-columns"]

    def valid_row(self) -> dict[str, str]:
        row = {column: "" for column in self.columns}
        row.update(
            {
                "record_id": "BR-ES-TEST-001",
                "country_code": "BR",
                "country_name": "Brazil",
                "state_code": "ES",
                "state_name": "Espírito Santo",
                "state_id": "32",
                "municipality_name": "Vitória",
                "municipality_slug": "vitoria",
                "municipality_id": "3205309",
                "location_precision": "municipality",
                "service": "radio_amateur",
                "callsign": "TEST",
                "rx_frequency_mhz": "145.0000",
                "modulation": "FM",
                "source_type": "official_documentation",
                "source_name": "Test source",
                "source_url": "https://example.test/source",
                "source_accessed_date": "2026-01-01",
                "verification_status": "official_documentation",
                "operational_status": "unknown",
                "redistribution_permission": "review_required",
            }
        )
        return row

    def write_rows(self, directory: Path, rows: list[dict[str, str]]) -> None:
        path = directory / "records.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_record_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_rows(root, [self.valid_row()])
            self.assertEqual(validate_tree(root), [])

    def test_missing_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["source_url"] = ""
            self.write_rows(root, [row])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertIn("source_url is required", messages)

    def test_duplicate_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = self.valid_row()
            second = self.valid_row()
            second["rx_frequency_mhz"] = "146.0000"
            self.write_rows(root, [first, second])
            self.assertTrue(any("duplicate record_id" in finding.message for finding in validate_tree(root)))

    def test_independent_reception_requires_date_and_method(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["source_type"] = "independent_reception"
            row["verification_status"] = "independently_verified"
            self.write_rows(root, [row])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertTrue(any("requires a verification date and method" in message for message in messages))

    def test_invalid_frequency_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["rx_frequency_mhz"] = "not-a-frequency"
            self.write_rows(root, [row])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertTrue(any("rx_frequency_mhz" in message for message in messages))

    def test_future_date_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["source_accessed_date"] = "2999-01-01"
            self.write_rows(root, [row])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertIn("source_accessed_date must not be in the future", messages)

    def test_publication_cannot_follow_access(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["source_publication_date"] = "2026-01-02"
            row["source_accessed_date"] = "2026-01-01"
            self.write_rows(root, [row])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertIn("source_publication_date must not be later than source_accessed_date", messages)

    def test_dmr_color_code_may_remain_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = self.valid_row()
            row["modulation"] = "digital"
            row["digital_protocol"] = "DMR"
            self.write_rows(root, [row])
            self.assertEqual(validate_tree(root), [])


class MunicipalityValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_schema(DEFAULT_MUNICIPALITY_SCHEMA)
        cls.columns = cls.schema["x-csv-columns"]

    @staticmethod
    def valid_row() -> dict[str, str]:
        return {
            "codigo_ibge": "3205309",
            "municipio": "Vitória",
            "uf": "ES",
            "pais": "BR",
        }

    def write_rows(self, directory: Path, rows: list[dict[str, str]]) -> None:
        path = directory / "municipios.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.columns)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_municipality_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_rows(root, [self.valid_row()])
            self.assertEqual(validate_tree(root), [])

    def test_duplicate_ibge_code_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = self.valid_row()
            second = {**self.valid_row(), "municipio": "Vila Velha"}
            self.write_rows(root, [first, second])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertTrue(any("duplicate codigo_ibge" in message for message in messages))

    def test_duplicate_municipality_name_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = self.valid_row()
            second = {**self.valid_row(), "codigo_ibge": "3205200", "municipio": "VITÓRIA"}
            self.write_rows(root, [first, second])
            messages = [finding.message for finding in validate_tree(root)]
            self.assertTrue(any("duplicate municipality name" in message for message in messages))

    def test_invalid_municipality_fields_are_rejected(self) -> None:
        cases = {
            "short code": ({**self.valid_row(), "codigo_ibge": "32053"}, "codigo_ibge has invalid format"),
            "wrong UF": ({**self.valid_row(), "uf": "XX"}, "uf has unsupported value"),
            "wrong country": ({**self.valid_row(), "pais": "US"}, "pais has unsupported value"),
            "empty name": ({**self.valid_row(), "municipio": ""}, "municipio is required"),
            "mismatched prefix": ({**self.valid_row(), "codigo_ibge": "3304557"}, "prefix does not match UF ES"),
        }
        for label, (row, expected) in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.write_rows(root, [row])
                messages = [finding.message for finding in validate_tree(root)]
                self.assertTrue(any(expected in message for message in messages), messages)

    def test_municipalities_are_not_treated_as_frequency_records(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_rows(root, [self.valid_row()])
            frequency_test = ValidatorTests()
            frequency_test.columns = load_schema(DEFAULT_SCHEMA)["x-csv-columns"]
            frequency_test.write_rows(root, [frequency_test.valid_row()])
            self.assertEqual(validate_tree(root), [])


if __name__ == "__main__":
    unittest.main()
