from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from radiosync.integrations.radioreference import RadioReferenceClient, RadioReferenceConfig


class RadioReferenceBoundaryTests(unittest.TestCase):
    def test_credentials_are_not_exposed_by_repr(self) -> None:
        config = RadioReferenceConfig("user", "secret-password", "secret-key")
        rendered = repr(config)
        self.assertNotIn("secret-password", rendered)
        self.assertNotIn("secret-key", rendered)

    def test_missing_environment_is_rejected(self) -> None:
        names = ["RADIOREFERENCE_USERNAME", "RADIOREFERENCE_PASSWORD", "RADIOREFERENCE_APP_KEY"]
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError) as context:
                RadioReferenceConfig.from_environment()
        for name in names:
            self.assertIn(name, str(context.exception))

    def test_client_is_disabled(self) -> None:
        client = RadioReferenceClient(RadioReferenceConfig("user", "password", "key"))
        with self.assertRaises(NotImplementedError):
            client.fetch_for_personal_programming()


if __name__ == "__main__":
    unittest.main()
