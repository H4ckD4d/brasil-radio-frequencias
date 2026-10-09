# RadioReference integration boundary

This directory is a deliberately disabled scaffold. It exists to keep any future licensed integration separate from RadioSync's public CSV database.

Before implementation:

1. Obtain an approved application key for the exact personal radio-programming workflow.
2. Require each user to authenticate with their own eligible account.
3. Confirm permitted caching, retention, display, transformation, and export behavior.
4. Complete a security review covering secrets and response logging.
5. Use synthetic fixtures only; never commit real SOAP responses.

Credentials are read only from `RADIOREFERENCE_USERNAME`, `RADIOREFERENCE_PASSWORD`, and `RADIOREFERENCE_APP_KEY`. The current client never connects to the service.

RadioReference data must not be written into `dados/`, committed, used to train models, or included in public exports without explicit permission covering that use.
