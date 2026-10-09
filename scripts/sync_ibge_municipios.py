"""Synchronize RadioSync municipal geography from official IBGE data."""

import argparse
import csv
import gzip
import json
import re
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["codigo_ibge", "municipio", "uf", "pais"]

UF_CODES = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29,
    "CE": 23, "DF": 53, "ES": 32, "GO": 52, "MA": 21,
    "MT": 51, "MS": 50, "MG": 31, "PA": 15, "PB": 25,
    "PR": 41, "PE": 26, "PI": 22, "RJ": 33, "RN": 24,
    "RS": 43, "RO": 11, "RR": 14, "SC": 42, "SP": 35,
    "SE": 28, "TO": 17,
}


def slugify(name):
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def fetch_municipalities(uf, code):
    url = (
        "https://servicodados.ibge.gov.br/api/v1/"
        f"localidades/estados/{code}/municipios"
    )
    request = urllib.request.Request(
        url, headers={"User-Agent": "RadioSync/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
        if raw.startswith(b"\x1f\x8b"):
            raw = gzip.decompress(raw)
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"Invalid IBGE response for {uf}")
    if len({str(item["id"]) for item in data}) != len(data):
        raise ValueError(f"Duplicate IBGE code in {uf}")
    return sorted(data, key=lambda item: item["nome"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply", action="store_true",
        help="Create missing municipal CSV indexes and directories"
    )
    args = parser.parse_args()

    total = 0
    pending = []

    for uf, code in sorted(UF_CODES.items()):
        municipalities = fetch_municipalities(uf, code)
        total += len(municipalities)

        slugs = [slugify(item["nome"]) for item in municipalities]
        if len(set(slugs)) != len(slugs):
            raise ValueError(f"Municipality directory collision in {uf}")

        csv_path = ROOT / "dados" / uf / "municipios.csv"
        if csv_path.exists():
            print(f"{uf}: {len(municipalities)} registros; CSV existente preservado")
            continue

        pending.append((uf, municipalities, slugs))
        print(f"{uf}: {len(municipalities)} registros; CSV pendente")

    print(f"\nTOTAL NACIONAL: {total}")
    print(f"UFs pendentes: {len(pending)}")

    if not args.apply:
        print("SIMULACAO: nenhum arquivo geográfico foi modificado.")
        return

    for uf, municipalities, slugs in pending:
        state_dir = ROOT / "dados" / uf
        state_dir.mkdir(parents=True, exist_ok=True)

        csv_path = state_dir / "municipios.csv"
        with csv_path.open("x", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for item in municipalities:
                writer.writerow({
                    "codigo_ibge": str(item["id"]),
                    "municipio": item["nome"],
                    "uf": uf,
                    "pais": "BR",
                })

        for slug in slugs:
            folder = state_dir / slug
            folder.mkdir(parents=True, exist_ok=True)
            marker = folder / ".gitkeep"
            if not any(folder.iterdir()):
                marker.touch(exist_ok=True)

        print(f"{uf}: estrutura geográfica criada")

    print("SINCRONIZACAO CONCLUIDA.")


if __name__ == "__main__":
    main()
