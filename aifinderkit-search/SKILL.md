---
name: aifinderkit-search
description: Search and extract current web information through the AI Finder Kit aggregate Search API. Use when the user asks to search the web, compare sources, collect current evidence, batch several queries, fetch readable page text, or assemble a research bundle with provenance through api.aifinderkit.com.
---

# AI Finder Kit Search

Version: `1.3.1`

Use the bundled dependency-free client to query the authenticated aggregate search service. For an interactive local installation, run `configure` to store the key in a protected file; for automation, inject `AIFINDERKIT_API_KEY`. Never place a key in prompts, command output, source files, or skill files.

## Requirements

- Python 3.10 or newer with outbound HTTPS access.
- A valid AI Finder Kit search or owner key in `AIFINDERKIT_API_KEY` or the protected credential file created by `configure`.
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
   - For scholarly work, use `--preset academic-strict`; use `academic-relaxed` only when project pages and non-paper technical reports are also useful. Relaxed mode trades precision for recall, so inspect `retrieval_signals.query_relevance` and discard weak matches.
   - `meta`: current access tier and request limits.
3. Run `scripts/aifinderkit_search.py`.
4. Use `retrieval_score` with its `retrieval_signals` when judging retrieval quality. The fusion `score` is only a provider-ranking value. `confidence` is a deprecated alias for `retrieval_score` and never represents factual truth.
5. Cite the returned page URLs in the user-facing answer. Treat snippets as discovery aids; use `fetch` or the primary page before making precise claims.
6. For comparisons or consequential claims, require either a primary source or agreement between two independent sources. Do not treat `confidence` as factual verification; it is a retrieval signal.

## Commands

```bash
python scripts/aifinderkit_search.py search "query" --limit 10 --mode balanced
python scripts/aifinderkit_search.py search "query" --language zh --category news
python scripts/aifinderkit_search.py search "query" --include-domain github.com
python scripts/aifinderkit_search.py domains --domain academic --domain code
python scripts/aifinderkit_search.py search "transformer" --vertical-domain academic --vertical-sub-domain academic.search
python scripts/aifinderkit_search.py search "multimodal learning" --preset academic-strict --mode deep
python scripts/aifinderkit_search.py research "retrieval augmented generation evaluation" --preset academic-strict --fetch-top 5
python scripts/aifinderkit_search.py batch --query "paper one" --query "paper two" --preset academic-relaxed --limit 5
python scripts/aifinderkit_search.py fetch "https://example.com/page"
python scripts/aifinderkit_search.py map "https://example.com/docs" --max-links 30
python scripts/aifinderkit_search.py crawl "https://example.com/docs" --max-pages 5 --max-depth 1
python scripts/aifinderkit_search.py research "topic" --subquery "history" --subquery "current evidence" --fetch-top 3
python scripts/aifinderkit_search.py meta
python scripts/aifinderkit_search.py configure
secret-manager-command | python scripts/aifinderkit_search.py configure --key-stdin
python scripts/aifinderkit_search.py doctor
```

Use `fast` for latency-sensitive discovery, `balanced` by default, and `deep` for research. Add `--freshness day|week|month|year` only when the request is time-bounded. The client timeout defaults to 60 seconds; for multi-PDF research, place `--timeout 120` before the command name.

For finance, academic, code, health, legal, security, travel, and other structured AnySearch domains, run `domains` first. Copy only a returned `sub_domain` and include every required parameter with `--vertical-param key=value`; use an empty value when the directory marks a required parameter but none applies. If `domains` returns 403, continue with ordinary aggregate search instead of inventing a vertical schema.

When Workflow step 2 is a literature review, follow [references/academic-research.md](references/academic-research.md) instead of the ordinary search path. Academic presets use specialized scholarly engines, expose DOI/author/year/open-access metadata when available, and avoid general-web fallbacks in strict mode. Read [references/api.md](references/api.md) before programmatically consuming the `academic` object.

Use `map` before `crawl`. Keep crawl defaults unless the user needs a specific small documentation section. Crawling is static HTML, same-host, at most eight pages and depth two; it is not a browser automation tool.

For deep research, read [references/research-workflow.md](references/research-workflow.md) before choosing subqueries or interpreting `coverage` and `gaps`. For source selection and citation checks, read [references/source-quality.md](references/source-quality.md).

If the bundled script is not the current working directory, resolve it relative to this `SKILL.md` instead of assuming `scripts/` exists in the user's project.

The client first checks `AIFINDERKIT_API_KEY` for an inline key. If it is unset, the client reads the protected file selected by `AIFINDERKIT_API_KEY_FILE`, or `~/.config/aifinderkit/credentials` by default. Interactive `configure` reads without echo; `configure --key-stdin` supports secret-manager pipelines. Both write mode `0600` outside the Skill and current project. Never pass a key as a command-line argument.

If an endpoint returns `401`, ask the user to configure a valid search key. If it returns `429`, report the limit and do not loop retries. If `warnings` says a source is unavailable, state that the result set was degraded instead of implying full aggregation.

Read [references/api.md](references/api.md) only when exact schemas, endpoint mappings, or error behavior are needed.
