"""Disabled scaffold for a future authorized RadioReference SOAP client.

No SOAP dependency or operation is implemented. Real development must begin only
after API approval and a written decision on caching, display, and export rights.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


DEFAULT_WSDL_URL = "https://api.radioreference.com/soap2/?wsdl&v=latest"


@dataclass(frozen=True)
class RadioReferenceConfig:
    """Runtime-only user credentials and approved application key."""

    username: str
    password: str = field(repr=False)
    application_key: str = field(repr=False)
    wsdl_url: str = DEFAULT_WSDL_URL

    @classmethod
    def from_environment(cls) -> "RadioReferenceConfig":
        """Read credentials without logging, caching, or writing them to disk."""

        names = {
            "username": "RADIOREFERENCE_USERNAME",
            "password": "RADIOREFERENCE_PASSWORD",
            "application_key": "RADIOREFERENCE_APP_KEY",
        }
        values = {field_name: os.environ.get(variable, "") for field_name, variable in names.items()}
        missing = [variable for field_name, variable in names.items() if not values[field_name]]
        if missing:
            raise RuntimeError("Missing required RadioReference environment variables: " + ", ".join(missing))
        return cls(**values)


class RadioReferenceClient:
    """Non-operational boundary that prevents accidental API use."""

    def __init__(self, config: RadioReferenceConfig) -> None:
        self._config = config

    def fetch_for_personal_programming(self, *_args: object, **_kwargs: object) -> None:
        """Refuse access until the approved SOAP contract is implemented."""

        raise NotImplementedError(
            "RadioReference access is disabled. Obtain API approval and implement "
            "per-user, non-persistent personal programming access before enabling it."
        )
