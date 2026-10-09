"""RadioSync - Tests for public source import preview.

Creator: h4ckd4d
"""

import contextlib
import csv
import io
import sys
import tempfile
import unittest

from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import import_public_sources as importer


class PublicSourceImporterTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        self.file = Path(self.temp.name) / "candidato.csv"

        self.source = {
            "nome": "Fonte ficticia para testes",
            "categoria": "estacoes_licenciadas",
            "licenca": "allowed",
            "importacao_automatica": False,
        }

        self.schema = importer.load_schema(importer.SCHEMA)
        self.row = {
            key: ""
            for key in self.schema["x-csv-columns"]
        }

        self.row.update({
            "record_id": "TEST-001",
            "country_code": "BR",
            "country_name": "Brazil",
            "state_code": "ES",
            "state_name": "Espírito Santo",
            "state_id": "32",
            "municipality_name": "Iconha",
            "municipality_slug": "iconha",
            "municipality_id": "3202603",
            "service": "amateur_radio",
            "rx_frequency_mhz": "145.3100",
            "modulation": "FM",
            "source_type": "official_documentation",
            "source_name": "Fonte ficticia",
            "source_url": "https://example.org/documento",
            "source_accessed_date": date.today().isoformat(),
            "verification_status": "official_documentation",
            "operational_status": "unknown",
            "redistribution_permission": "allowed_with_attribution",
            "data_license": "CC-BY-4.0",
            "attribution": "Fonte ficticia",
        })

    def write_csv(self):
        with self.file.open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=self.schema["x-csv-columns"],
            )
            writer.writeheader()
            writer.writerow(self.row)

    def run_preview(self, source=None, existing=None):
        output = io.StringIO()

        if source is None:
            source = self.source

        if existing is None:
            existing = (set(), set())

        with patch.object(
            importer, "existing_records",
            return_value=existing
        ):
            with contextlib.redirect_stdout(output):
                result = importer.preview(source, self.file)

        return result, output.getvalue()

    def test_registered_sources_are_locked(self):
        sources = importer.load_sources()

        for source in sources.values():
            self.assertEqual(
                source["licenca"], "review_required"
            )
            self.assertFalse(
                source["importacao_automatica"]
            )

    def test_restricted_source_is_blocked(self):
        self.write_csv()

        source = dict(self.source)
        source["licenca"] = "restricted"

        result, _ = self.run_preview(source)

        self.assertEqual(result, 2)

    def test_wrong_category_is_blocked(self):
        self.write_csv()

        source = dict(self.source)
        source["categoria"] = "atribuicao_de_faixas"

        result, _ = self.run_preview(source)

        self.assertEqual(result, 2)

    def test_missing_file_is_reported(self):
        result, _ = self.run_preview()

        self.assertEqual(result, 1)

    def test_invalid_csv_is_rejected(self):
        self.file.write_text(
            "record_id\nTEST-001\n",
            encoding="utf-8"
        )

        result, _ = self.run_preview()

        self.assertEqual(result, 1)

    def test_duplicate_record_id_is_detected(self):
        self.write_csv()

        result, output = self.run_preview(
            existing=({"TEST-001"}, set())
        )

        self.assertEqual(result, 2)
        self.assertIn("Duplicados: 1", output)

    def test_duplicate_technical_key_is_detected(self):
        self.write_csv()

        key = importer.technical_key(self.row)

        result, output = self.run_preview(
            existing=(set(), {key})
        )

        self.assertEqual(result, 2)
        self.assertIn("Duplicados: 1", output)

    def test_valid_candidate_is_read_only(self):
        self.write_csv()

        before = self.file.read_bytes()

        result, output = self.run_preview()

        after = self.file.read_bytes()

        self.assertEqual(result, 0)
        self.assertEqual(before, after)
        self.assertIn("Candidatos novos: 1", output)
        self.assertIn("Registros importados: 0", output)

    def test_invalid_source_type_is_rejected(self):
        self.row["source_type"] = "operator_report"
        self.write_csv()

        result, output = self.run_preview()

        self.assertEqual(result, 2)
        self.assertIn(
            "Incompativeis com o escopo: 1",
            output
        )

    def test_restricted_record_must_be_blocked(self):
        """A permitted source cannot override row-level rights."""

        self.row["redistribution_permission"] = "restricted"
        self.write_csv()

        result, _ = self.run_preview()

        self.assertEqual(
            result, 2,
            "Registro restrito nao pode ser aprovado."
        )


if __name__ == "__main__":
    unittest.main()