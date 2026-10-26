# Guidance for learning agents

Read `rule.md`, `observability-roadmap.md`, and the active numbered project's
`readme.md` before continuing. Those guides are included in this repository.

Teach one project at a time with short notebook cells and simple helpers.
Give one explained snippet, its target file, how to run it, and the expected
result. Wait for the learner's `next` or equivalent before the next snippet.

Inspect or run the learner's work when they request `-check`, or when an explicit
edit, review, or repository audit requires reading the relevant files. Keep that
work within the requested scope. Never print credentials. Do not rerun model
calls merely to recover results already saved in a notebook.

All lessons use the shared root uv environment. Preserve the numbered folders
and their `docs/`, `models/`, `prompts/`, `tools/`, notebook, and README layout.
Use `tools/prepare_data.py` for Project 3's explicit preparation command.

Project 3's core flow is documented and has saved examples. Wait for the learner
to choose to continue before starting Project 4. Reference answers remain
drafts until human review.
