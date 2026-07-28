# Academic research workflow

Use this workflow instead of SKILL.md Workflow step 2 when the task is a literature review.

1. Start with `search --preset academic-strict --mode deep`. Strict mode uses scholarly engines and never falls back to Bing or ordinary AnySearch.
2. Use `academic-relaxed` only when lab pages, project sites, datasets, standards, or technical reports are part of the question. It deliberately favors recall; inspect `retrieval_signals.query_relevance`, especially below `0.35`, and exclude results that do not answer the query.
3. Prefer results carrying DOI, authors, publication year, venue, and an academic engine/domain signal. `retrieval_score` measures retrieval quality, not whether a claim is true.
4. Run `research --preset academic-strict --fetch-top 5` with explicit subquestions. When a legal open-access PDF is known, research fetches it instead of merely reading the publisher landing page.
5. Cite only fetched evidence. Record DOI and page metadata when available; treat abstracts and snippets as discovery leads.
6. Check `is_retracted` when present, `is_oa`, `metadata_sources`, `enrichment_status`, extraction failures, and coverage gaps. Retraction status is optional and currently depends on a configured source such as direct OpenAlex enrichment. Never bypass a login or paywall.

`enrichment_status` reports only the direct external metadata-enrichment attempt. `not_found`, `error`, or `timeout` does not erase DOI, author, venue, or PDF metadata already supplied by a search engine. See [api.md](api.md) for the complete academic response contract.
