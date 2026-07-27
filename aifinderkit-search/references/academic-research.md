# Academic research workflow

1. Start with `search --preset academic-strict --mode deep`. Strict mode uses scholarly engines and never falls back to Bing or ordinary AnySearch.
2. Use `academic-relaxed` only when lab pages, project sites, datasets, standards, or technical reports are part of the question.
3. Prefer results carrying DOI, authors, publication year, venue, and an academic engine/domain signal. `retrieval_score` measures retrieval quality, not whether a claim is true.
4. Run `research --preset academic-strict --fetch-top 5` with explicit subquestions. When a legal open-access PDF is known, research fetches it instead of merely reading the publisher landing page.
5. Cite only fetched evidence. Record DOI and page metadata when available; treat abstracts and snippets as discovery leads.
6. Check `is_retracted`, `is_oa`, `metadata_sources`, extraction failures, and coverage gaps. Never bypass a login or paywall.
