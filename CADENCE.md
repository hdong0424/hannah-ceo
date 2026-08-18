# Coffee Cadence

A read-only re-entry workflow for the Hannah CEO repository.

## Trigger words

- 咖啡
- coffee

When Hannah uses either trigger word, help her recover the current state of the repository before choosing the next action.

## Run the evidence collector

From the repository root, run:

```text
python3 tools/coffee.py
```

The tool returns a read-only Markdown evidence packet containing:

- `README.md`;
- `ROADMAP.md` and its declared current focus;
- the current project's `README.md`;
- the most recent actual decision record;
- the most recent actual coding note, if one exists;
- the latest Git commit;
- and the current Git working-tree status.

Use only that evidence packet to prepare the cadence response. Do not silently replace missing evidence with memory or assumptions. Do not treat directory instructions or templates as completed records.

## Return five answers

1. What am I currently trying to accomplish?
2. What was the last meaningful thing I completed?
3. What did I learn or decide?
4. What remains uncertain or unfinished?
5. What is the smallest useful action I can understand and attempt next?

## Evidence rules

Clearly label each statement as:

- **Fact:** directly recorded in the repository or Git history.
- **Inference:** a reasonable interpretation of the available evidence.
- **Recommendation:** a proposed next action that Hannah may accept, change, or reject.

If the repository does not contain an answer, say:

> The repository does not currently contain this information.

Do not invent missing progress, decisions, lessons, or objectives.

## Response style

- Use Chinese as the primary language.
- Use English only when it adds clarity or identifies an existing technical term.
- Keep the summary concise and understandable.
- Report uncommitted changes clearly, but do not automatically make them the highest-priority next action.
- Offer between two and four genuinely different paths.
- Label the paths with capital letters: **A**, **B**, **C**, and, when needed, **D**.
- Never provide more than four paths.
- Recommend one lettered path and explain why.
- Stop and let Hannah make the final decision.

## Safety boundary

This workflow is read-only.

Do not modify files, create records, commit, push, deploy, publish, or communicate with another person unless Hannah gives separate and explicit approval.
