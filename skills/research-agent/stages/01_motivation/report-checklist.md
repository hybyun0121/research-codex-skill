# Motivation Report Checklist

Use this checklist before marking Motivation complete.

## Required Content

- Research question is stated clearly.
- Search facets are listed.
- Tool usage and provenance are recorded.
- English report exists.
- Korean report exists.
- Literature landscape includes source links.
- Themes and main baselines are summarized.
- Gaps are evidence-backed.
- Candidate directions are scored.
- Selected direction is explicit.
- Handoff to Method is complete.
- Open questions are listed.

## Tool Usage Requirements

The report must state which tools were used for literature search and analysis.

For each tool, record:

- tool name;
- tool type: `mcp`, `web`, `local_script`, `manual_import`, or `other`;
- provider, if relevant;
- purpose;
- queries or inputs;
- outputs used in the report;
- limitations or missing coverage.

## Language Requirements

- Write `research/motivation.md` in English.
- Write `research/motivation.ko.md` in Korean.
- Preserve identical source links, tool provenance, candidate scores, and Method handoff content across both versions.
- Keep technical terms in English when Korean translation would reduce precision.
- Do not translate paper titles, venue names, benchmark names, dataset names, method names, or metric names unless a field-standard Korean name exists.

Examples:

- `Semantic Scholar MCP` used for paper search and citation metadata.
- `OpenAlex MCP` used for venue/concept metadata and citation links.
- `arXiv API` used for latest preprint search.
- `Paper Reader MCP` used for Introduction, Related Work, Experiments, and Limitations extraction.
- `NotebookLM import` used as supporting notes only, with original paper links preserved.

## Evidence Quality

- Do not cite a tool output without source links.
- Do not treat imported summaries as primary evidence.
- Separate `paper claim`, `agent inference`, and `user preference`.
- Do not overstate novelty until close baselines and citation-neighbor papers have been checked.
