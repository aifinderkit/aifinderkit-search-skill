---
name: aifinderkit-search
description: Search and extract current web information through the AI Finder Kit aggregate Search API. Use when the user asks to search the web, compare sources, collect current evidence, batch several queries, fetch readable page text, or assemble a research bundle with provenance through api.aifinderkit.com.
---

# AI Finder Kit Search

Version: `1.2.0` (development)

Use the bundled dependency-free client to query the authenticated aggregate search service. Keep the API key in `AIFINDERKIT_API_KEY`; never place it in prompts, command output, source files, or skill files.

## Requirements

- Python 3.10 or newer with outbound HTTPS access.
- A valid AI Finder Kit search or owner key in `AIFINDERKIT_API_KEY`.
- No extra Python packages. This skill bundle intentionally contains no credentials.

Before the first search, run `python scripts/aifinderkit_search.py doctor`. It verifies Python, authentication, the API version, available endpoints, and current limits without printing the key.

## Workflow

1. Run `doctor` when access has not been verified in the current environment.
2. Choose the smallest operation that answers the request:
   - `search`: one query with normalized, deduplicated results.
   - `domains`: discover valid AnySearch vertical sub-domains before a structured search.
   - `batch`: two to five independent queries.
   - `fetch`: readable text from a known public HTTP(S) page.
   - `map`: discover a bounded list of links on one static page.
   - `crawl`: extract a small same-host section, never a broad site crawl.
   - `research`: multi-query evidence collection, extraction, coverage, and gap detection.
   - `meta`: current access tier and request limits.
3. Run `scripts/aifinderkit_search.py`.
4. Use result `sources`, `engines`, `created_at`, and `cached` fields when judging evidence quality and freshness.
5. Cite the returned page URLs in the user-facing answer. Treat snippets as discovery aids; use `fetch` or the primary page before making precise claims.
6. For comparisons or consequential claims, require either a primary source or agreement between two independent sources. Do not treat `confidence` as factual verification; it is a retrieval signal.

## Commands

```bash
python scripts/aifinderkit_search.py search "query" --limit 10 --mode balanced
python scripts/aifinderkit_search.py search "query" --language zh --category news
python scripts/aifinderkit_search.py search "query" --include-domain github.com
python scripts/aifinderkit_search.py domains --domain academic --domain code
python scripts/aifinderkit_search.py search "transformer" --vertical-domain academic --vertical-sub-domain academic.search
python scripts/aifinderkit_search.py batch --query "first" --query "second"
python scripts/aifinderkit_search.py fetch "https://example.com/page"
python scripts/aifinderkit_search.py map "https://example.com/docs" --max-links 30
python scripts/aifinderkit_search.py crawl "https://example.com/docs" --max-pages 5 --max-depth 1
python scripts/aifinderkit_search.py research "topic" --subquery "history" --subquery "current evidence" --fetch-top 3
python scripts/aifinderkit_search.py meta
python scripts/aifinderkit_search.py doctor
```

Use `fast` for latency-sensitive discovery, `balanced` by default, and `deep` for research. Add `--freshness day|week|month|year` only when the request is time-bounded.

For finance, academic, code, health, legal, security, travel, and other structured AnySearch domains, run `domains` first. Copy only a returned `sub_domain` and include every required parameter with `--vertical-param key=value`; use an empty value when the directory marks a required parameter but none applies. If `domains` returns 403, continue with ordinary aggregate search instead of inventing a vertical schema.

Use `map` before `crawl`. Keep crawl defaults unless the user needs a specific small documentation section. Crawling is static HTML, same-host, at most eight pages and depth two; it is not a browser automation tool.

For deep research, read [references/research-workflow.md](references/research-workflow.md) before choosing subqueries or interpreting `coverage` and `gaps`. For source selection and citation checks, read [references/source-quality.md](references/source-quality.md).

If the bundled script is not the current working directory, resolve it relative to this `SKILL.md` instead of assuming `scripts/` exists in the user's project.

If an endpoint returns `401`, ask the user to configure a valid search key. If it returns `429`, report the limit and do not loop retries. If `warnings` says a source is unavailable, state that the result set was degraded instead of implying full aggregation.

Read [references/api.md](references/api.md) only when exact schemas, endpoint mappings, or error behavior are needed.
