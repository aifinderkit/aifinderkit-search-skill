---
name: aifinderkit-search
description: Search and extract current web information through the AI Finder Kit aggregate Search API. Use when the user asks to search the web, compare sources, collect current evidence, batch several queries, fetch readable page text, or assemble a research bundle with provenance through api.aifinderkit.com.
---

# AI Finder Kit Search

Version: `1.1.0` (2026-07-27)

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
   - `batch`: two to five independent queries.
   - `fetch`: readable text from a known public HTTP(S) page.
   - `research`: search plus extraction of the top pages.
   - `meta`: current access tier and request limits.
3. Run `scripts/aifinderkit_search.py`.
4. Use result `sources`, `engines`, `created_at`, and `cached` fields when judging evidence quality and freshness.
5. Cite the returned page URLs in the user-facing answer. Treat snippets as discovery aids; use `fetch` or the primary page before making precise claims.

## Commands

```bash
python scripts/aifinderkit_search.py search "query" --limit 10 --mode balanced
python scripts/aifinderkit_search.py batch --query "first" --query "second"
python scripts/aifinderkit_search.py fetch "https://example.com/page"
python scripts/aifinderkit_search.py research "topic" --fetch-top 3
python scripts/aifinderkit_search.py meta
python scripts/aifinderkit_search.py doctor
```

Use `fast` for latency-sensitive discovery, `balanced` by default, and `deep` for research. Add `--freshness day|week|month|year` only when the request is time-bounded.

If the bundled script is not the current working directory, resolve it relative to this `SKILL.md` instead of assuming `scripts/` exists in the user's project.

If an endpoint returns `401`, ask the user to configure a valid search key. If it returns `429`, report the limit and do not loop retries. If `warnings` says a source is unavailable, state that the result set was degraded instead of implying full aggregation.

Read [references/api.md](references/api.md) only when exact schemas, endpoint mappings, or error behavior are needed.
