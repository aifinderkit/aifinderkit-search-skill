# Research Workflow

Use this workflow only when one search cannot support the requested synthesis.

1. State the research question and identify two to five non-overlapping subquestions. Prefer dimensions such as official position, implementation evidence, current status, limitations, and alternatives; do not create paraphrases of the same query.
2. Run `research` with the root question and the subquestions. Keep `fetch_top` at three by default and never above five.
3. Inspect `coverage`, `gaps`, `matched_queries`, source diversity, and extraction failures before drafting.
4. If a material gap remains, run one targeted `search` or `batch` round. Do not repeat broad searches indefinitely.
5. Use `evidence_matrix` citation IDs in working notes. Map every consequential claim to fetched content from at least one primary source or two independent supporting sources. Verify the cited passage in `evidence[].document.content`; a URL or snippet alone is not support.
6. Report disagreements and unavailable evidence explicitly. Never turn a retrieval `confidence` score into confidence in the truth of a claim.
7. Cite direct result URLs in the final answer. Prefer the page that contains the evidence, not a search page or aggregator.

Stop after two retrieval rounds unless the user explicitly requests exhaustive research. This keeps latency and upstream usage bounded on the shared gateway.
