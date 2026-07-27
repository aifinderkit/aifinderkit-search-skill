# AI Finder Kit Search API

Base URL: `https://api.aifinderkit.com/v1`

Authentication: `Authorization: Bearer $AIFINDERKIT_API_KEY`

Client compatibility: Python 3.10+; no third-party packages required. Run `python scripts/aifinderkit_search.py doctor` after installation to verify authentication and capability discovery without exposing the key.

## Endpoints

### `POST /search`

Input: `query` (required), `limit` (1–30), `mode` (`fast`, `balanced`, `deep`), optional `freshness`, `language`, and `categories`.

Output contains `results[]` with `title`, canonical `url`, `snippet`, `published_at`, `sources`, `engines`, `rank`, and fusion `score`. Top-level fields include `sources_used`, `warnings`, `cached`, and `created_at`.

### `POST /batch-search`

Input: `queries` (one to five strings) plus shared search options. Output `items[]` contains ordinary search responses.

### `POST /fetch`

Input: `url` and optional `max_chars` (1,000–100,000). The service accepts public HTTP(S) HTML/text only, validates DNS and every redirect, blocks non-global addresses, caps downloads, and returns extracted readable text.

### `POST /research`

Input: `query`, `limit`, `fetch_top` (0–5), and optional `freshness`. Output includes a search response and extracted `documents[]`. A document may contain `error: "fetch unavailable"` when the page blocks extraction.

### `GET /search/meta`

Returns the access tier, supported operations, and limits granted to the current key. Available source providers depend on that tier and may change without requiring a client update.

## Errors

- `401`: missing or invalid bearer key.
- `413`: fetched page exceeds the byte cap.
- `415`: URL does not return supported text/HTML.
- `422`: invalid request schema.
- `429`: per-minute or daily limit reached.
- `502`: all relevant sources are unavailable.

Never automatically retry `401`, `413`, `415`, or `422`. For `429`, wait for the published window or ask the user to review their quota. A `200` response with non-empty `warnings` is usable but degraded.
