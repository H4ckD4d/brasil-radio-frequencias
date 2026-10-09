"""RadioSync - Preview seguro de importacao de fontes publicas.

Criador: h4ckd4d
Slogan: Do sinal a informacao. Do Brasil para o mundo.

Esta versao executa somente simulacoes.
Nao baixa fontes e nao grava registros.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

from validate_csv import load_schema, validate_file

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "fontes" / "catalogo_fontes.json"
SCHEMA = ROOT / "schemas" / "frequency-record.schema.json"
DATA = ROOT / "dados"

ALLOWED = {"allowed", "allowed_with_attribution"}

KEY_FIELDS = (
    "country_code",
    "state_code",
    "municipality_id",
    "locality_id",
    "service",
    "callsign",
    "channel_designator",
    "rx_frequency_mhz",
    "tx_frequency_mhz",
)


def load_sources():
    with CATALOG.open(encoding="utf-8-sig") as file:
        data = json.load(file)
    return {item["id"]: item for item in data["fontes"]}


def technical_key(row):
    return tuple(row[field] for field in KEY_FIELDS)


def existing_records():
    ids = set()
    keys = set()

    for path in sorted(DATA.rglob("*.csv")):
        if path.name == "municipios.csv":
            continue

        with path.open(
            newline="", encoding="utf-8-sig"
        ) as file:
            for row in csv.DictReader(file):
                ids.add(row["record_id"])
                keys.add(technical_key(row))

    return ids, keys


def list_sources(sources):
    print("=== RADIOSYNC - FONTES CADASTRADAS ===")

    for source_id, source in sorted(sources.items()):
        print(f"\nID: {source_id}")
        print(f"Nome: {source['nome']}")
        print(f"Categoria: {source['categoria']}")
        print(f"Licenca: {source['licenca']}")
        print(
            "Importacao automatica: "
            f"{source['importacao_automatica']}"
        )

    print(f"\nTotal de fontes: {len(sources)}")
    print("Nenhum arquivo foi modificado.")


def preview(source, input_path):
    print("=== RADIOSYNC - PREVIEW DE IMPORTACAO ===")
    print(f"Fonte: {source['nome']}")
    print(f"Arquivo candidato: {input_path}")
    print("Modo: SOMENTE LEITURA")

    if source["licenca"] not in ALLOWED:
        print("BLOQUEADO: permissao de redistribuicao pendente.")
        return 2

    if source["categoria"] != "estacoes_licenciadas":
        print(
            "BLOQUEADO: esta fonte nao representa "
            "registros individuais de estacoes."
        )
        return 2

    if not input_path.is_file():
        print("ERRO: arquivo candidato nao encontrado.")
        return 1

    schema = load_schema(SCHEMA)

    findings, rows = validate_file(
        input_path, schema, record_type="frequency"
    )

    if findings:
        for finding in findings:
            print(finding)
        print(f"VALIDACAO REPROVADA: {len(findings)} problema(s).")
        return 1

    current_ids, current_keys = existing_records()

    new_ids = set()
    new_keys = set()
    duplicates = 0
    candidates = 0
    invalid = 0

    for row in rows:
        record_id = row["record_id"]
        key = technical_key(row)

        if (
            record_id in current_ids
            or key in current_keys
            or record_id in new_ids
            or key in new_keys
        ):
            duplicates += 1
            continue

        if (
            row["country_code"] != "BR"
            or row["source_type"] != "official_documentation"
            or row["redistribution_permission"] not in ALLOWED
        ):
            invalid += 1
            continue

        new_ids.add(record_id)
        new_keys.add(key)
        candidates += 1

    print("\n=== RESULTADO DA SIMULACAO ===")
    print(f"Registros analisados: {len(rows)}")
    print(f"Candidatos novos: {candidates}")
    print(f"Duplicados: {duplicates}")
    print(f"Incompativeis com o escopo: {invalid}")
    print("Registros importados: 0")
    print("Nenhum arquivo foi modificado.")

    if duplicates or invalid:
        print("REVISAO NECESSARIA antes de qualquer importacao.")
        return 2

    print("SIMULACAO CONCLUIDA - REVISAO HUMANA PENDENTE")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="RadioSync - Importador seguro (dry-run)"
    )

    parser.add_argument(
        "--list-sources", action="store_true"
    )
    parser.add_argument("--source")
    parser.add_argument("--input", type=Path)

    args = parser.parse_args()

    sources = load_sources()

    if args.list_sources and not args.source and not args.input:
        list_sources(sources)
        return 0

    if not args.source or not args.input:
        parser.error(
            "Informe --source e --input ou use --list-sources."
        )

    if args.source not in sources:
        print(f"ERRO: fonte desconhecida: {args.source}")
        return 1

    return preview(sources[args.source], args.input)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        print(f"ERRO: {exc}")
        sys.exit(1)