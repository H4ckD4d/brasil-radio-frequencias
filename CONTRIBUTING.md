# Contributing to RadioSync

Thank you for helping build a reliable radio-frequency reference. Accuracy, provenance, lawful use, and licensing are more important than record count.

## Ways to contribute

- Add a documented frequency or geographic area.
- Submit a dated, independently verified reception report.
- Correct inaccurate, expired, or incomplete metadata.
- Report a duplicate or an unavailable source.
- Improve validation, importers, exporters, tests, or documentation.

Use the applicable Issue form for discussion or open a focused Pull Request.

## Data contribution requirements

Every submitted record must:

1. Follow [the canonical CSV format](docs/DATA_FORMAT.md).
2. Cite an HTTPS source URL and provide meaningful attribution.
3. Identify the source as official documentation, an operator report, a community submission, a secondary compilation, or independent reception.
4. Record the source publication date when known.
5. State whether redistribution is allowed, restricted, or still requires review.
6. Keep operational status at `unknown` unless a source reports it or an independent observation verifies it.
7. Avoid personal information that is not necessary and lawfully publishable.

Do not copy content from subscription databases, closed groups, private messages, or restrictive websites merely because it can be viewed. Public accessibility is not the same as redistribution permission.

## Independent reception reports

Use `source_type=independent_reception` only for direct observation. Include:

- UTC or clearly identified local date.
- General verification method and receiving equipment class.
- Enough context to distinguish the station or channel.
- No private message content or personal identifiers.

An observed carrier alone does not establish station identity. If identity is uncertain, submit an Issue instead of asserting a match.

## Workflow

1. Fork the repository and create a narrowly scoped branch.
2. Edit or add CSV files without deleting unrelated records.
3. Run:

   ```bash
   python scripts/validate_csv.py
   python -m unittest discover -s tests -v
   ```

4. Explain each source, transformation, and uncertainty in the Pull Request.
5. Respond to review without rewriting other contributors' attribution.

Keep Pull Requests small. Data corrections and software changes should normally be separate.

## Workspace safety

Keep the active Git working tree on a local, non-synchronized filesystem when possible. Consumer sync tools such as Google Drive can upload `.git` internals while Git is updating them, create conflicted copies, or expose a partially synchronized repository to another computer. Use Git remotes for repository synchronization and use cloud storage only for closed archives or backups.

If a synchronized workspace is unavoidable, never open the same checkout on two computers, allow synchronization to finish before and after Git operations, and check for conflict copies or `.git/*.lock` files before continuing. Do not delete a lock file until no Git process is running and the repository has been backed up. Run `git status` and `git fsck` after any sync conflict.

## Record identity and corrections

`record_id` is stable. Do not change it solely because a label or status changes. Correct facts in place and explain the evidence in the Pull Request. If two records are duplicates, request a reviewed merge; do not silently delete either record.

## Attribution and authorship

RadioSync was created by [h4ckd4d](https://github.com/H4ckD4d). Preserve that project attribution.

Contributors must not claim ownership of work they did not create. Credit source authors and organizations in the record, and credit contributors through commits, Pull Requests, and [AUTHORS.md](AUTHORS.md) when appropriate. Contributors retain authorship of their original contributions; inclusion does not assign ownership of unrelated code or data.

## Licensing

No repository-wide license has been adopted yet. See [the licensing proposal](docs/LICENSING_PROPOSAL.md). By submitting material, you confirm that you have the right to contribute it and will identify any applicable source terms. A maintainer may hold a contribution until its licensing is clear.

## Conduct and security

Follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report security problems through [SECURITY.md](SECURITY.md), not a public data-correction Issue.
