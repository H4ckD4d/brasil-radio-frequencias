# RadioSync CSV Data Format

Schema version: **1.0.0**

The canonical column order and machine-readable constraints are defined in [`schemas/frequency-record.schema.json`](../schemas/frequency-record.schema.json). All CSV files use UTF-8, a header row, comma separators, decimal points, and ISO 8601 dates (`YYYY-MM-DD`). Empty optional values remain empty; never guess.

## Identity and geography

| Field | Requirement |
|---|---|
| `record_id` | Stable, globally unique RadioSync identifier. |
| `country_code` | ISO 3166-1 alpha-2 code, such as `BR`. |
| `country_name` | English country name. |
| `state_code` | State/province code used by the country. |
| `state_name` | Official state/province name. |
| `state_id` | Authoritative geographic identifier; Brazilian rows use the two-digit IBGE UF code. |
| `municipality_name` | Official municipality name; optional for state/national references. |
| `municipality_slug` | Lowercase ASCII path slug. |
| `municipality_id` | Authoritative identifier; Brazilian rows use the seven-digit IBGE code. |
| `locality_name`, `locality_id` | District, locality, or equivalent identifier when applicable. |
| `latitude`, `longitude` | Optional WGS 84 decimal coordinates; must appear together. |
| `location_precision` | `exact`, `approximate`, `municipality`, `state`, or `country`. |

Municipal directories use slugs for readable paths, but slugs are not stable identifiers. A district must not be represented as a municipality.

## Station and frequency

| Field | Requirement |
|---|---|
| `service` | Controlled lowercase value, such as `amateur_radio`, `aviation`, or `maritime`. |
| `station_name` | Published station/site name, if available. |
| `callsign` | Assigned callsign; do not place generic channel labels here. |
| `channel_designator` | Published channel or functional label such as `CH16`. |
| `rx_frequency_mhz` | Frequency received by the programmed radio, with 4–6 decimal places. |
| `tx_frequency_mhz` | Frequency transmitted by the programmed radio; optional for receive-only references. |
| `modulation` | Controlled modulation value. Digital systems use `digital`. |
| `digital_protocol` | Protocol such as `DMR`, `P25`, `TETRA`, `AIS`, or `DSC`. |
| `ctcss_hz`, `dcs_code` | Analog access parameters when documented. |
| `dmr_color_code`, `dmr_timeslot` | DMR parameters when documented. |
| `repeater_offset_mhz` | Signed `TX - RX` offset. Leave empty rather than derive it when the input is uncertain. |

RX and TX are from the perspective of the user's programmed radio. For a repeater, RX is normally the repeater output and TX is normally the repeater input.

## Provenance

| Field | Requirement |
|---|---|
| `source_type` | One of the source classes in [DATA_SOURCES.md](DATA_SOURCES.md). |
| `source_claim` | The source's original status/context claim, without upgrading it. |
| `source_name` | Human-readable publication or organization name. |
| `source_url` | Absolute HTTPS URL. |
| `source_publication_date` | Publication/update date, when known. |
| `source_accessed_date` | Date the linked source was checked. |
| `last_independently_verified_date` | Date of direct independent verification; not the source date. |
| `verification_method` | Concise method for an independent observation. |
| `verification_status` | `official_documentation`, `source_only`, `independently_verified`, `disputed`, or `unverified`. |
| `operational_status` | `unknown`, `reported_active`, `reported_inactive`, `verified_active`, `verified_inactive`, or `not_applicable`. |

`official_documentation` is evidence that a document exists. It is not evidence of current radio activity. `reported_*` repeats a source's claim. `verified_*` requires a dated independent verification.

## Rights and notes

| Field | Requirement |
|---|---|
| `redistribution_permission` | `allowed`, `allowed_with_attribution`, `restricted`, or `review_required`. |
| `data_license` | SPDX identifier, license URL/name, or source-specific rights statement. |
| `attribution` | Credit required by the source or contributor. |
| `notes` | Scope, expiry, ambiguity, limitations, and other factual context. |

Public exporters must include only `allowed` and `allowed_with_attribution` rows and must carry forward required attribution. `restricted` and `review_required` records are never eligible by default.

## Duplicate policy

The validator rejects duplicate `record_id` values and duplicate technical keys consisting of geography, service, callsign/channel, RX, and TX. Similar records from different sources should not be collapsed automatically; open a reviewed correction and retain provenance.

## Example

The following abbreviated example is illustrative only and is not a real frequency record:

```csv
record_id,country_code,country_name,state_code,state_name,state_id,municipality_name,municipality_slug,municipality_id,service,rx_frequency_mhz,modulation,source_type,source_name,source_url,verification_status,operational_status,redistribution_permission
EXAMPLE-001,BR,Brazil,ES,Espírito Santo,32,Vitória,vitoria,3205309,amateur_radio,145.0000,FM,community_submission,Example source,https://example.invalid/source,unverified,unknown,review_required
```

Real files must contain every canonical column in schema order.
