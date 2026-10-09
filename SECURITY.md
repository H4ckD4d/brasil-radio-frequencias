# Security Policy

## Supported versions

RadioSync is pre-release software. Security fixes are applied to the current `main` branch; no released version is currently supported.

## Reporting a vulnerability

Do not open a public Issue for vulnerabilities, exposed credentials, private information, or a path that could publish restricted data.

Prefer GitHub's private vulnerability reporting feature for this repository when available. Otherwise, contact the maintainer privately through the contact options on [h4ckd4d's GitHub profile](https://github.com/H4ckD4d) and provide:

- A concise description and affected files or versions.
- Reproduction steps or a minimal proof of concept.
- Likely impact.
- Suggested mitigation, if known.

Do not access data beyond what is needed to demonstrate the issue. Do not include RadioReference credentials, session tokens, private user data, or licensed API responses in a report.

## What belongs elsewhere

An inaccurate frequency, stale operational report, or broken public source link is normally a data-quality issue. Use the correction Issue form unless disclosure would expose private or restricted information.

## Secrets policy

Credentials must be supplied at runtime through environment variables or an approved secret store. They must never appear in source files, CSV records, fixtures, logs, Issues, Pull Requests, or generated exports.
