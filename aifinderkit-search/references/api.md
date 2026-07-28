# AI Finder Kit Search API

Base URL: `https://api.aifinderkit.com/v1`

Authentication: `Authorization: Bearer $AIFINDERKIT_API_KEY`

Client compatibility: Python 3.10+; no third-party packages required. Run `python scripts/aifinderkit_search.py doctor` after installation to verify authentication and capability discovery without exposing the key.

## Endpoints

### `POST /search`

Input: `query` (required), `limit` (1–30), `mode` (`fast`, `balanced`, `deep`), optional `preset` (`academic-relaxed` or `academic-strict`), `freshness`, `language`, `categories`, `include_domains`, and `exclude_domains`.

Output contains `results[]` with `title`, canonical `url`, cleaned query-centered `snippet`, `published_at`, `sources`, `engines`, `domain`, `source_type`, `match_reasons`, `retrieved_at`, `rank`, and the scores described below. Top-level fields include `sources_used`, `enrichment_sources`, `queries_used`, `warnings`, `duration_ms`, `cached`, and `created_at`. Top-level `metadata_sources` is a deprecated compatibility alias for `enrichment_sources`.

Score semantics:

- `score`: weighted reciprocal-rank fusion value used to order provider candidates; do not compare it across unrelated requests.
- `retrieval_score`: normalized retrieval-quality score recommended for result selection.
- `retrieval_signals`: components of `retrieval_score`: `query_relevance`, `rank`, `source_diversity`, `metadata_completeness`, `source_authority`, and `academic_evidence`.
- `confidence`: deprecated alias for `retrieval_score`, identified by `confidence_semantics: "deprecated_alias_for_retrieval_score"`; it is not factual confidence.

Academic results contain an `academic` object:

| Field | Meaning |
|---|---|
| `score` | Strength of academic classification signals, not paper quality |
| `query_relevance` | Query relevance derived from title and snippet |
| `signals[]` | Reasons such as `academic_search_engine`, `doi_available`, or `query_terms_matched` |
| `doi`, `authors[]`, `year`, `venue` | Normalized bibliographic metadata when available |
| `pdf_url`, `is_oa` | Legal open-access PDF discovery; never implies paywall bypass |
| `is_retracted` | Optional retraction flag when a configured source supplies it |
| `metadata_sources[]` | Direct external enrichment sources for this result |
| `enrichment_status` | `not_attempted`, `not_configured`, `not_needed`, `no_doi`, `enriched`, `not_found`, `error`, or `timeout` |
| `oa_source`, `oa_version`, `landing_page_url` | Optional open-access location details supplied by enrichment |

`enrichment_status` describes direct external enrichment only. A result marked `not_found`, `error`, `timeout`, or `not_configured` may still carry DOI, author, venue, and PDF fields obtained from the search engine. `metadata_sources` inside `academic` is scoped to that result; top-level `enrichment_sources` is the union of successful direct enrichment sources across the request.

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

Input: `query`, optional `subqueries` (up to five), `limit`, `fetch_top` (0–5), optional academic `preset`, and shared search filters. The root query uses `deep`; explicit subqueries use `balanced`. Output contains `searches[]`, merged `results[]`, extracted `evidence[]`, `evidence_matrix[]`, `coverage`, and machine-readable `gaps`. For academic results, an available legal open-access PDF is fetched before the landing page. Evidence entries retain the result metadata, stable `S1`-style citation ID, DOI/author/year/PDF fields, and SHA-256 of fetched text. A failed document contains `error: "fetch unavailable"`; never cite it as evidence.

### `GET /search/meta`

Returns the access tier, supported operations, academic presets, mode time budgets, outbound/fetch concurrency caps, and limits granted to the current key. Available source providers depend on that tier and may change without requiring a client update.

## Errors

- `401`: missing or invalid bearer key.
- `413`: fetched page exceeds the byte cap.
- `415`: URL does not return supported text/HTML.
- `422`: invalid request schema.
- `429`: per-minute or daily limit reached.
- `502`: all relevant sources are unavailable.

Never automatically retry `401`, `413`, `415`, or `422`. For `429`, wait for the published window or ask the user to review their quota. A `200` response with non-empty `warnings` is usable but degraded.
