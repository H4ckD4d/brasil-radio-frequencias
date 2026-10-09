# Licensing Proposal — Maintainer Approval Required

No license is currently granted for this repository. This document is a proposal, not a license notice, and does not change copyright ownership or third-party terms.

## Recommended separation

### Software: Apache License 2.0

Use Apache-2.0 for Python code, schemas, workflows, and software documentation authored for RadioSync. It is permissive, requires preservation of notices, and includes an express patent grant that is useful for an international tooling project.

Alternative: MIT is shorter and widely understood but does not provide the same express patent language.

### Project-authored data: CC BY 4.0

Use CC BY 4.0 only for original database selection/arrangement and records that contributors have the right to license. It supports sharing and adaptation while requiring attribution and addresses database rights in jurisdictions where they apply.

CC0 would maximize reuse but is not the preferred initial recommendation because RadioSync explicitly values durable source and contributor attribution. ODbL could enforce share-alike database terms but creates additional compatibility and operational complexity.

## Exclusions

A future project data license must not relicense:

- RadioReference content.
- Third-party records marked `restricted` or `review_required`.
- Personal information or content submitted without authority.
- Source documents merely linked from a record.
- Any dataset whose license requires different terms.

Per-record source permissions override project defaults. Restricted records should ultimately be removed from distributable branches or replaced with independently sourced, lawfully reusable facts before a public release.

## Decision checklist

- Confirm the copyright holder name to place in software notices.
- Decide whether contributor code is accepted under Apache-2.0.
- Decide whether eligible project-authored data is CC BY 4.0, CC0, or ODbL.
- Define how pre-license contributions will be approved for relicensing.
- Audit every existing row before labeling a public data release.
- Add actual license files only after the maintainer records the decision.
