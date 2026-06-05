# Motivation

## Goal

Build the existing-study landscape and identify a novel, worth-solving research direction.

## Default Criteria

1. Worth solving: the problem affects important capability, cost, risk, scientific understanding, or deployment.
2. Existing limitation: prior work leaves a measurable gap, assumption, failure mode, or unsupported setting.
3. Novel resolution: the idea changes mechanism, objective, data, evaluation, or theory in a way that could close the gap.
4. Feasibility: the project can be executed with available data, compute, time, and tools.
5. Verifiability: the claim can be tested with credible baselines and falsifiable metrics.

## Workflow

1. Convert the research question or baseline repo into search facets.
2. Gather related work from trusted sources, prioritizing recent papers from credible venues.
3. Use external tools such as NotebookLM or Liner AI when available, but preserve source links.
4. Build a landscape matrix: paper, venue/year, task, method, contribution, limitation, link.
5. Cluster papers into themes.
6. Identify gaps and candidate directions.
7. Score candidates against criteria.
8. Ask the user to choose, merge, or revise only when the downstream method depends on it.

## Output

Write `research/motivation.md` and update:

- `research.question`
- `research.domain`
- `research.selected_direction`
- `motivation.criteria`
- `motivation.landscape`
- `motivation.gaps`
- `motivation.candidates`

