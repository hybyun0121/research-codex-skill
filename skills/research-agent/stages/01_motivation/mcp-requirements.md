# Motivation MCP Requirements

## Purpose

The Motivation stage needs tooling for paper discovery, paper reading, citation graph exploration, literature memory, and user decisions. Use MCP servers when available, and fall back to local scripts or manual source links when unavailable.

## Required Capabilities

### 1. Scholarly Search

Recommended tools:

- `search_papers(query, filters)`
- `get_paper_detail(paper_id)`
- `get_related_papers(paper_id)`
- `get_references(paper_id)`
- `get_citations(paper_id)`

Preferred providers:

- Semantic Scholar for paper search, citation metadata, and recommendations.
- OpenAlex for open scholarly metadata, works, concepts, venues, and citation links.
- arXiv for preprints and latest papers.

Fallback:

- use web search and manually fill `paper.schema.json` fields with source links.

### 2. Paper Reader / PDF Parser

Recommended tools:

- `fetch_pdf(url)`
- `extract_sections(pdf_or_url, sections)`
- `extract_tables(pdf_or_url)`
- `extract_claims(text_or_pdf)`
- `extract_limitations(text_or_pdf)`

Useful sections:

- abstract
- introduction
- related work
- method
- experiments
- limitations
- conclusion

Fallback:

- summarize only from accessible abstract/introduction/limitations text and mark missing sections as unknown.

### 3. Citation Graph

Recommended tools:

- `expand_backward_citations(seed_papers, depth)`
- `expand_forward_citations(seed_papers, depth)`
- `find_sibling_papers(seed_papers)`
- `find_surveys(seed_query)`
- `rank_seminal_and_recent_papers(papers)`

Output should distinguish:

- seminal papers;
- closest baselines;
- recent competitive papers;
- survey papers;
- underexplored branches.

Fallback:

- use references/citations from Semantic Scholar or OpenAlex if graph traversal tools are unavailable.

### 4. Literature Store

Recommended resources/tools:

- `literature://papers`
- `literature://landscape`
- `store_paper(paper)`
- `store_summary(paper_id, summary)`
- `mark_excluded(paper_id, reason)`
- `list_seen_papers()`

Default local storage:

- `.research-agent/literature.jsonl`
- optional `.research-agent/literature.sqlite`

The store should track:

- seen papers;
- excluded papers;
- source links;
- extracted limitations;
- candidate gaps;
- user decisions.
- tool usage provenance for the final Motivation report.

### 5. User Elicitation

Recommended tools:

- `ask_research_question_start_mode`
- `ask_topic_criteria_override`
- `ask_candidate_direction_choice`
- `ask_scope_constraint`

Question rules:

- ask only when a decision blocks progress;
- provide a recommended option first;
- provide 2-3 choices plus a custom answer path;
- use Korean/English mixed user-facing language for Motivation questions;
- keep technical option labels in English, such as `Baseline-driven gap discovery`, `Direct research question`, and `Domain-first candidate generation`;
- write the reason and recommendation in Korean unless the user requests English-only;
- record the selected option in `.research-agent/decisions.jsonl`.

## Optional Capabilities

### Novelty Scoring

Recommended tool:

- `score_candidate_topic(candidate, landscape, criteria)`

Use scores from `candidate-topic.schema.json`.

### Venue / Benchmark Filter

Recommended tools:

- `filter_by_venue(papers, venues)`
- `filter_recent_competitive_papers(papers, year_range)`
- `extract_main_table_reference(paper)`

### Citation Manager

Recommended tools:

- `generate_bibtex(paper_ids)`
- `dedupe_papers(papers)`
- `export_references(format)`

### External Note Import

Recommended tools:

- `import_notebooklm_notes(path_or_export)`
- `import_liner_sources(path_or_export)`

Do not treat imported summaries as primary evidence unless the original paper/source links are preserved.

## Reporting Requirement

Any MCP/tool used during Motivation must be recorded in the final report's `Tool Usage And Provenance` section and in `.research-agent/motivation_report.json`.

Minimum fields:

- tool name;
- tool type;
- provider;
- purpose;
- queries or inputs;
- outputs used;
- limitations.

The same tool usage record must appear in both `research/motivation.md` and `research/motivation.ko.md`.
