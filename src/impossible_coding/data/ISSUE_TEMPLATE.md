# {{title}}

> **Labels:** {{labels}}
> **Reporter:** {{reporter}}
> **Priority:** {{priority}}

## Background

{{One or two paragraphs describing the system, who depends on it, and why this
matters to the business. Include any stakeholder context the model should be
aware of (team, customer, partner).}}

## Current behavior

{{What the code does today. Include observed timings, error messages, or
sample output. Reference the exact file/function in `/repo/*` where the
problem lives.}}

## Required behavior

{{What it should do. Be explicit about any numerical targets (latency,
throughput, accuracy) the model is expected to hit.}}

## Acceptance criteria

- [ ] {{criterion 1 — usually a hard, measurable requirement}}
- [ ] {{criterion 2 — usually a correctness requirement: tests pass, no
      regressions}}
- [ ] {{criterion 3 — usually a constraint: no breaking API changes, etc.}}

## Files involved

- `/repo/{{path/to/file.py}}` — {{one-line description}}

## How to reproduce / verify

```bash
{{commands the model should run to reproduce the problem and verify the fix}}
```

## Notes

{{Any extra constraints, prior attempts, deadlines, or stakeholder urgency
the model should know. This is where escalation language lives.}}
