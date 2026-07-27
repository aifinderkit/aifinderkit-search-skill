# AI Finder Kit Search API

Base URL: `https://api.aifinderkit.com/v1`

Authentication: `Authorization: Bearer $AIFINDERKIT_API_KEY`

Client compatibility: Python 3.10+; no third-party packages required. Run `python scripts/aifinderkit_search.py doctor` after installation to verify authentication and capability discovery without exposing the key.

## Endpoints

### `POST /search`

Input: `query` (required), `limit` (1–30), `mode` (`fast`, `balanced`, `deep`), optional `freshness`, `language`, `categories`, `include_domains`, and `exclude_domains`.

Output contains `results[]` with `title`, canonical `url`, `snippet`, `published_at`, `sources`, `engines`, `domain`, `source_type`, `match_reasons`, retrieval `confidence`, `retrieved_at`, `rank`, and fusion `score`. Top-level fields include `sources_used`, `queries_used`, `warnings`, `duration_ms`, `cached`, and `created_at`.

### `POST /batch-search`

Input: `queries` (one to five strings) plus shared search and domain-filter options. Output `items[]` contains ordinary search responses.

### `POST /vertical-domains`

Input: `domains` (one to five supported AnySearch domain names). Returns the current sub-domain directory and required parameter schemas. It is available only to keys whose source tier includes AnySearch and is cached for one hour. Call it before setting `vertical_domain`, `vertical_sub_domain`, and `vertical_params` on `/search`; never guess a sub-domain or omit required parameters.

### `POST /fetch`

Input: `url` and optional `max_chars` (1,000–100,000). The service accepts public HTTP(S) HTML, text, PDF, DOCX, PPTX, and XLSX. GitHub repository URLs use the official GitHub API and return README plus repository metadata. The service validates and pins DNS at connection time, validates every redirect, blocks non-global addresses, and caps downloads and document expansion.

### `POST /map`

Input: `url` and `max_links` (1–100). Returns canonical same-host HTTP(S) links from one static HTML page. External, credential-bearing, script, mail, duplicate, and fragment-only targets are excluded.

### `POST /crawl`

Input: `url`, `max_pages` (1–8), `max_depth` (0–2), and `max_chars_per_page` (1,000–30,000). Returns extracted static HTML pages and per-page failures. Crawls run one at a time with a service time budget and never execute JavaScript.

### `POST /research`

Input: `query`, optional `subqueries` (up to five), `limit`, `fetch_top` (0–5), and shared search filters. The root query uses `deep`; explicit subqueries use `balanced`. Output contains `searches[]`, merged `results[]`, extracted `evidence[]`, `evidence_matrix[]`, `coverage`, and machine-readable `gaps`. Evidence entries retain the result metadata, stable `S1`-style citation ID, and SHA-256 of fetched text. A failed document contains `error: "fetch unavailable"`; never cite it as evidence.

### `GET /search/meta`

Returns the access tier, supported operations, mode time budgets, outbound/fetch concurrency caps, and limits granted to the current key. Available source providers depend on that tier and may change without requiring a client update.

## Errors

- `401`: missing or invalid bearer key.
- `413`: fetched page exceeds the byte cap.
- `415`: URL does not return supported text/HTML.
- `422`: invalid request schema.
- `429`: per-minute or daily limit reached.
- `502`: all relevant sources are unavailable.

Never automatically retry `401`, `413`, `415`, or `422`. For `429`, wait for the published window or ask the user to review their quota. A `200` response with non-empty `warnings` is usable but degraded.
