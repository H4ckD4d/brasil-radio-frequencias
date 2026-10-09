"""Validate RadioSync official source registry.

Project: RadioSync - Brasil Radio Frequencias
Creator: h4ckd4d
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "fontes" / "catalogo_fontes.json"

REQUIRED = {
    "id",
    "nome",
    "url",
    "categoria",
    "cobertura",
    "licenca",
    "importacao_automatica",
    "observacao",
}

PERMISSIONS = {
    "allowed",
    "allowed_with_attribution",
    "restricted",
    "review_required",
}


def validate():
    errors = []

    if not CATALOG.is_file():
        return ["Catalogo de fontes nao encontrado."]

    with CATALOG.open(encoding="utf-8-sig") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        return ["Estrutura principal deve ser um objeto JSON."]

    sources = data.get("fontes")

    if not isinstance(sources, list) or not sources:
        return ["Lista de fontes ausente ou vazia."]

    ids = set()
    urls = set()

    for index, source in enumerate(sources, start=1):

        if not isinstance(source, dict):
            errors.append(f"Fonte {index}: formato invalido.")
            continue

        missing = REQUIRED - source.keys()

        if missing:
            errors.append(
                f"Fonte {index}: campos ausentes: {sorted(missing)}"
            )
            continue

        source_id = source["id"]

        if not isinstance(source_id, str) or not re.fullmatch(
            r"[a-z0-9_]+", source_id
        ):
            errors.append(f"Fonte {index}: ID invalido.")
            continue

        if source_id in ids:
            errors.append(f"ID duplicado: {source_id}")

        ids.add(source_id)

        for field in ("nome", "categoria", "cobertura", "observacao"):
            value = source[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{source_id}: campo {field} invalido."
                )

        url = source["url"]

        if not isinstance(url, str):
            errors.append(f"{source_id}: URL invalida.")
        else:
            parsed = urlparse(url)

            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                errors.append(f"{source_id}: URL HTTPS invalida.")

            if url in urls:
                errors.append(f"{source_id}: URL duplicada.")

            urls.add(url)

        permission = source["licenca"]

        if permission not in PERMISSIONS:
            errors.append(
                f"{source_id}: permissao desconhecida."
            )

        automatic = source["importacao_automatica"]

        if not isinstance(automatic, bool):
            errors.append(
                f"{source_id}: importacao_automatica deve ser booleana."
            )

        elif automatic and permission not in {
            "allowed",
            "allowed_with_attribution",
        }:
            errors.append(
                f"{source_id}: importacao automatica nao autorizada."
            )

    print("=== RADIOSYNC - VALIDACAO DE FONTES ===")
    print(f"Fontes analisadas: {len(sources)}")
    print(f"Erros encontrados: {len(errors)}")

    return errors


def main():
    try:
        errors = validate()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}")
        return 1

    if errors:
        for error in errors:
            print(f"ERRO: {error}")
        return 1

    print("VALIDACAO APROVADA")
    print("Nenhum arquivo de dados foi modificado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())