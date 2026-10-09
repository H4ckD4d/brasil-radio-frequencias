# RadioSync Roadmap

The roadmap is evidence-driven. Dates are intentionally omitted until maintainers approve release scope and licensing.

## Phase 1 — Foundation

- [x] Canonical international CSV schema.
- [x] Provenance, verification, operational-state, and redistribution fields.
- [x] Standard-library validator and unit tests.
- [x] Pull Request validation workflow.
- [x] Community documentation and contribution templates.
- [x] Creator/maintainer attribution.
- [x] Disabled RadioReference integration boundary.
- [ ] Maintainer decision on software and data licensing.
- [ ] Resolve redistribution status of all retained third-party records.

## Phase 2 — Espírito Santo data quality

- Build the complete IBGE municipality/district catalog for Espírito Santo.
- Correct the current municipality/district directory ambiguity around Itaipava.
- Add immutable source manifests and transformation logs.
- Review every existing repeater entry against an authorized source.
- Collect dated local verification without publishing private communications.
- Add expiry checks for temporary aviation notices.

## Phase 3 — Official-source ingestion

- Implement reproducible IBGE geographic imports.
- Evaluate and integrate appropriate Anatel open datasets.
- Preserve source snapshots only where redistribution permits it.
- Add checksums, retrieval dates, field mappings, and change reports.
- Keep authorization/licensing state separate from observed operation.

## Phase 4 — Programming exports

- Add CHIRP profiles with equipment-aware field limits.
- Add SDR channel-list exports.
- Evaluate documented Uniden-compatible workflows.
- Exclude restricted and review-required rows from public exports.
- Add deterministic builds and round-trip tests where formats allow.

## Phase 5 — Authorized RadioReference workflow

- Obtain API approval for the precise personal programming use case.
- Confirm caching, retention, display, and export permissions in writing.
- Implement per-user authentication without credential persistence.
- Keep licensed responses isolated from public data and telemetry.
- Add synthetic contract tests; never commit real API payloads.

## Phase 6 — Brazil and international expansion

- Add all Brazilian states through the same source-controlled process.
- Introduce country-specific geographic identifier adapters.
- Add translated contributor guidance without changing canonical semantics.
- Provide a query/API layer backed by generated SQLite or PostgreSQL data.
- Establish releases with signed manifests and documented data provenance.
