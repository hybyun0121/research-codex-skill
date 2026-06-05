# Motivation

## Goal

Build the existing-study landscape and identify a novel, worth-solving research direction.

## Required Context

- Current repo profile from `.research-agent/repo_profile.json`.
- Existing run state from `.research-agent/state.json`, if present.
- User-provided research question, domain, target venue level, or baseline preference.
- Available MCP/tooling from `mcp-requirements.md`.

## User Communication Policy

During the Motivation stage, talk with the user in Korean/English mixed style:

- Keep technical research terms in English: `Motivation`, `research question`, `literature landscape`, `baseline`, `novelty`, `gap`, `candidate direction`, `MCP`, `schema`, `citation graph`, `paper reader`, `leaderboard`.
- Use Korean for ordinary explanation, guidance, progress updates, and user-facing questions.
- When asking the user to choose, write the reason and recommendation in Korean while keeping option labels technically precise.
- Preserve paper titles, venue names, benchmark names, dataset names, and quoted source terms in their original language.
- If an artifact explicitly requires English, such as final slides, keep that artifact in English. `research/motivation.md` may use English section headings and technical terms, but explanatory notes for the user can be Korean/English mixed unless the user requests English-only.

Example question style:

```text
Motivation 방향을 정하려면 starting point가 필요해요.
Recommended: Baseline-driven gap discovery
Reason: 현재 repo에 baseline signal이 있으니, 먼저 related work와 limitation을 잡는 편이 좋아요.

Options:
1. Baseline-driven gap discovery
2. Direct research question 입력
3. Domain-first candidate generation
```

## Default Criteria

1. Worth solving: the problem affects important capability, cost, risk, scientific understanding, or deployment.
2. Existing limitation: prior work leaves a measurable gap, assumption, failure mode, or unsupported setting.
3. Novel resolution: the idea changes mechanism, objective, data, evaluation, or theory in a way that could close the gap.
4. Feasibility: the project can be executed with available data, compute, time, and tools.
5. Verifiability: the claim can be tested with credible baselines and falsifiable metrics.
6. Baseline availability: the selected direction has credible prior methods or official code that can anchor later experiments.

## Workflow

1. Determine the starting mode:
   - empty repo: ask for a domain or research question;
   - baseline repo: inspect README/paper/code signals and start from novelty gap discovery;
   - existing project: summarize current direction and ask whether to resume, audit, or reframe.
2. Convert the research question or baseline repo into search facets:
   - task;
   - method family;
   - dataset or benchmark;
   - failure mode;
   - target venue or field;
   - time window.
3. Gather related work from trusted sources, prioritizing recent papers from credible venues.
4. Use MCP tools in this order when available:
   - scholarly search;
   - paper reader/PDF parser;
   - citation graph;
   - literature store;
   - user elicitation.
5. Use external tools such as NotebookLM or Liner AI only as importable supporting evidence. Preserve source links and do not treat unsupported summaries as primary evidence.
6. Build a landscape matrix using `landscape.schema.json`.
7. Cluster papers into themes and identify:
   - common assumptions;
   - main baselines;
   - unresolved limitations;
   - benchmark gaps;
   - method-level opportunities.
8. Score candidate topics using `candidate-topic.schema.json`.
9. Recommend 2-3 candidate directions with tradeoffs.
10. Ask the user to choose, merge, or revise only when the downstream Method stage depends on it.

## Evidence Rules

- Attach source links to claims, limitations, benchmark statements, and venue/year metadata.
- Prefer official paper pages, proceedings, arXiv/OpenReview/ACL Anthology/ACM/IEEE/Springer pages, official code, and trusted benchmark pages.
- Separate "paper claim", "agent inference", and "user preference".
- If a claim is inferred from multiple papers, list the supporting papers.
- Do not overstate novelty before checking close baselines and citation-neighbor papers.

## Handoff To Method

The selected direction must include:

- problem statement;
- prior limitation being addressed;
- proposed novelty mechanism;
- closest baseline papers;
- expected method object or intervention;
- minimum experiment evidence needed later.

## Motivation Report

At the end of this stage, write a user-readable Motivation report and a structured report object:

- `research/motivation.md`: readable report based on `report-template.md`;
- `.research-agent/motivation_report.json`: structured report following `motivation-report.schema.json`.

The report must include `Tool Usage And Provenance`. Record every MCP, web, local script, or manual import used for paper search, paper reading, citation graph exploration, novelty scoring, and user elicitation.

Before marking Motivation complete, check `report-checklist.md`.

## Output

Write `research/motivation.md` and update:

- `research.question`
- `research.domain`
- `research.selected_direction`
- `motivation.search_facets`
- `motivation.criteria`
- `motivation.landscape`
- `motivation.themes`
- `motivation.gaps`
- `motivation.candidates`
- `motivation.selected_direction_handoff`
- `motivation.tool_usage`
- `motivation.report_path`
