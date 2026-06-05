# Method

## Goal

Turn the selected research direction into a rigorous method specification through a bounded user-agent co-design loop.

This stage starts after Motivation has already identified the research direction, gap or novelty context, and related-work landscape. It prepares a handoff-ready method specification for the later Experiments stage, but it does not design experiments.

## Inputs From Motivation

- selected research direction
- motivation summary, gap, and novelty context
- related-work landscape already gathered in the Motivation stage
- closest prior methods already identified from that landscape

## Non-goals

- Do not repeat literature search or external research-tool work.
- Do not design baselines, metrics, dashboards, leaderboards, hyperparameter sweeps, or experiment execution.
- Do not reframe the selected direction unless the user confirms the change.

## Decision Boundaries

The agent may autonomously:

- clean up notation;
- make assumptions explicit;
- structure pseudocode;
- propose a diagram or visualization plan;
- improve plain-language explanation;
- organize rigor-review findings.

The agent must ask the user before:

- changing the core method mechanism;
- changing the novelty claim;
- introducing or changing a key assumption;
- reframing the selected direction from Motivation.

## Workflow

1. Clarify the method claim from the selected direction.
2. Connect the method claim to the Motivation gap and novelty context.
3. Define inputs, outputs, constraints, and expected method behavior.
4. Build a notation table for variables, symbols, dimensions, and meanings.
5. State assumptions and mark which ones require user confirmation.
6. Write the mathematical formulation where possible.
7. Define the objective, optimization target, or decision rule.
8. Produce an algorithm box for the main procedure.
9. Add a diagram or visualization plan that explains the mechanism.
10. Write a plain-language explanation for a research audience.
11. Check rigor:
   - undefined symbols
   - dimensional inconsistency
   - hidden assumptions
   - invalid optimization objective
   - data leakage
   - mismatch between novelty claim and formulation
   - weak connection to the Motivation gap
12. Compare against the closest prior methods using the already-gathered Motivation context.

## Output

Write `research/method.md` and update:

- `method.claim`
- `method.connection_to_motivation`
- `method.inputs`
- `method.outputs`
- `method.notation`
- `method.assumptions`
- `method.constraints`
- `method.formulation`
- `method.objective`
- `method.algorithm`
- `method.visuals`
- `method.plain_language_explanation`
- `method.rigor_review`
- `method.comparison_to_prior_work`
- `method.user_confirmation_required`
