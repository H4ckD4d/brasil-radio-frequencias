# Data Sources and Redistribution Policy

## Core rule

RadioSync records facts together with their provenance. A source being visible on the web does not establish permission to republish its database content. Every row carries a `redistribution_permission` value, and restricted material must never enter generated public exports.

## Source classes

| Class | Meaning | Independent operational proof? |
|---|---|---:|
| `official_documentation` | Regulator or competent authority publication | No |
| `operator_report` | Statement by the responsible operator | No |
| `community_submission` | Contributor report with supporting evidence | No |
| `secondary_compilation` | Third-party list or directory | No |
| `independent_reception` | Dated direct observation with a method | Yes, within its stated scope |
| `unknown` | Source type still under review | No |

Official authorization, allocation, or registration does not prove that a transmitter is active. Conversely, reception does not prove that a station is lawfully authorized.

## Current source register

### IBGE geographic identifiers

- Organization: Instituto Brasileiro de Geografia e Estatística (IBGE).
- Use: official country subdivision and Brazilian municipality identifiers.
- Reference: https://www.ibge.gov.br/explica/codigos-dos-municipios.php
- Treatment: cite IBGE and retain the retrieved identifier. Geographic metadata is not an operational-frequency source.

### Anatel Ato nº 883/2024

- Organization: Agência Nacional de Telecomunicações (Anatel).
- Use: Brazilian maritime VHF channel documentation.
- Reference: https://informacoes.anatel.gov.br/legislacao/atos-de-requisitos-tecnicos-de-gestao-do-espectro/2024/1918-ato-883
- Treatment: source attribution is required. Records describe nationally regulated channels and do not assert local activity.
- Update note: Ato nº 5018/2026 amended the requirements. Future reviews must compare affected fields before updating records.

### DECEA AISWEB NOTAM E6356/26

- Organization: Departamento de Controle do Espaço Aéreo (DECEA).
- Use: time-limited aviation coordination frequencies and context.
- Reference: https://aisweb.decea.mil.br/?i=notam&notam_id=12974142&view=single
- Treatment: official documentation, not an independently verified reception. Redistribution terms require review, so current rows are not marked redistributable.
- Validity note: the current records describe the validity window in `notes`; they must not be generalized into permanent aerodrome channels.

### “Levantamento ES 2025” on Scribd

- Displayed uploader: Cleverson PU1CAC.
- Use: secondary repeater compilation dated 2025-02-18.
- Reference: https://pt.scribd.com/document/838374672/Repetidoras-ES-e-Mantenedores-18022025
- Treatment: `restricted`. The displayed page states “All Rights Reserved.” The retained local records are source-only claims, not independent confirmations, and must not be included in redistributable exports unless permission or an independently sourced factual basis is documented.

### RepeaterBook references

Some legacy notes state that a station is also listed in RepeaterBook. No RepeaterBook record has been imported, no RepeaterBook URL is currently cited, and those notes are not independent verification. Do not scrape or import this source without reviewing its current terms and obtaining any required permission.

## RadioReference

RadioReference content is outside the public dataset. Its SOAP service is intended here only for future authorized personal radio-programming workflows in which each user supplies their own credentials and satisfies the service's subscription requirements.

- API information: https://support.radioreference.com/hc/en-us/articles/18844460198932-Database-Web-Service-API
- Terms: https://www.radioreference.com/terms/
- WSDL: https://api.radioreference.com/soap2/?wsdl&v=latest

Never commit credentials, SOAP responses, caches, or RadioReference database content. Do not transform licensed responses into public CSV data. Any broader caching, redistribution, directory, dashboard, or commercial use requires explicit permission covering that use.

## Adding a source

Before importing records:

1. Record the publisher, canonical URL, publication date, and access date.
2. Save the applicable license or terms reference.
3. Determine whether extraction and redistribution are permitted.
4. Document transformations and field mapping.
5. Assign the most conservative permission when terms are unclear: `review_required`.
6. Keep raw restricted content outside Git and outside public exports.
