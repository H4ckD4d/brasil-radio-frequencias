# RadioSync — Brasil Radio Frequências

RadioSync is an international, community-driven open-source project for documenting radio-frequency information and producing safe, traceable inputs for radio programming tools. The initial dataset covers Espírito Santo, Brazil, and is designed to expand across Brazil and other countries.

> A listed frequency is not proof that a station is currently operating. Every record must preserve its source, verification state, and redistribution status.

## Visão geral em português

O RadioSync organiza informações de radiofrequência por país, estado ou província, município e serviço de comunicação. A base inicial cobre o Espírito Santo e poderá crescer para outras regiões.

Os dados distinguem documentação oficial, relatos comunitários e recepções verificadas de forma independente. Uma frequência publicada não deve ser tratada automaticamente como ativa. Contribuições precisam apresentar fonte confiável, respeitar a legislação, a privacidade e as licenças dos dados.

Consulte [como contribuir](CONTRIBUTING.md), o [formato dos dados](docs/DATA_FORMAT.md) e as [fontes cadastradas](docs/DATA_SOURCES.md).

## Scope

RadioSync is intended to support:

- Amateur radio repeaters and simplex channels.
- Aviation and maritime reference channels.
- Analog and digital radio systems.
- SDR research and documented reception reports.
- Radio programming exports for compatible tools and equipment.
- Auditable geographic and source metadata.

The project does not authorize transmission, replace official publications, guarantee operational status, or grant rights to restricted third-party data.

## Data trust model

Each record identifies one source class:

- **Official documentation** — published by a regulator or other competent authority.
- **Operator report** — supplied by the responsible station or system operator.
- **Community submission** — supplied by a contributor with supporting evidence.
- **Secondary compilation** — transcribed from a third-party list and not independently confirmed.
- **Independent reception** — locally received and documented with a date and verification method.

Operational state is separate from regulatory or documentary state. Values such as `reported_active` only repeat a source's claim. Only a dated independent verification may use a `verified_*` state.

## Repository layout

```text
dados/                                  Canonical CSV datasets
schemas/frequency-record.schema.json    Machine-readable record schema
scripts/validate_csv.py                 Dependency-free CSV validator
tests/                                  Validator tests
docs/                                   Data and project documentation
radiosync/integrations/radioreference/  Disabled integration boundary
exports/                                Generated radio/SDR output targets
.github/                                Contribution templates and CI
```

CSV exports are generated artifacts and must not become the source of truth.

## Validate the data

Python 3.11 or newer is recommended. The validator uses only the standard library.

```bash
python scripts/validate_csv.py
python -m unittest discover -s tests -v
```

Validation checks canonical headers, required fields, frequency formatting, geographic identifiers, URLs, dates, verification claims, redistribution metadata, and duplicate records.

## Join the Project / Contribute

RadioSync welcomes:

- Amateur radio operators.
- Radio-frequency researchers.
- Radio communication technicians.
- SDR enthusiasts.
- Software developers.
- Radio equipment programmers.
- People who can verify information locally.

You can contribute verified frequencies, report outdated records, suggest corrections, add geographic coverage, improve documentation, write validators or exporters, and submit Pull Requests.

Every data contribution must include a reliable source and a clear redistribution status. Local reception reports must include a date and verification method. Do not submit private user information, credentials, confidential systems data, or third-party database content that cannot be redistributed.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) or open one of the repository's structured Issue forms.

## RadioReference boundary

RadioReference support is reserved for future authorized, per-user personal radio-programming workflows. Credentials, API responses, caches, and licensed database content must never be committed. RadioReference-derived content must not be merged into the public dataset without explicit redistribution permission. See [DATA_SOURCES.md](docs/DATA_SOURCES.md).

## Licensing status

No project license has been adopted yet. A separated software/data recommendation is documented in [LICENSING_PROPOSAL.md](docs/LICENSING_PROPOSAL.md). Until the maintainer approves and adds licenses, do not assume that repository content is licensed for reuse.

Individual source permissions recorded in CSV rows still apply and can be more restrictive than any future project-wide data license.

## Safety and legal notice

Use this project for lawful receiving, research, documentation, and authorized radio programming. Users are responsible for applicable spectrum rules, equipment authorization, privacy requirements, and local law. Never infer permission to transmit from the presence of a frequency.

## Creator and maintainer

**Created by [h4ckd4d](https://github.com/H4ckD4d)** — project creator and maintainer.

Original project attribution must be preserved. Contributors retain credit for their own work through Git history, Pull Requests, source attribution, and [AUTHORS.md](AUTHORS.md); contribution does not transfer authorship of unrelated work.
