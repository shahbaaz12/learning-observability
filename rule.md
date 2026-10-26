# Observability learning rules

The goal is to understand a small working application and its traces. Use these
rules for every lesson and implementation task in this repository.

## Learning workflow

1. Work on one project at a time. Begin the next lesson when the learner chooses
   to continue.
2. Use a numbered folder such as `1_basic_tracing` for each project. Preserve
   existing folder names and structure.
3. All projects share the repository root's `.venv`, `.env`, `pyproject.toml`,
   and `uv.lock`. The root was initialized with `uv init .` once. Use `uv sync`
   in a fresh clone and run notebooks in VS Code with the shared kernel.
4. Explain the goal, setup commands, and folder structure before implementation.
5. Give one small snippet at a time. State its target file or cell, what it does,
   how to run it, and what result to expect.
6. Stop after each snippet. Continue when the learner says `next` or equivalent.
   Do not require pasted output as the default condition for continuing.
7. Inspect or test the learner's work when they request `-check`. An explicit
   request to edit, review, or audit files authorizes the necessary reads and
   checks within that task's scope.
8. Keep the first working version simple: ordinary functions, simple assertions,
   no `try`/`except`, complex handlers, unnecessary classes, or production services.
9. Keep notebooks focused on explanations, settings, short calls, visible outputs,
   and comparisons. Put preparation, model/store setup, and reusable application
   or reporting logic in explained supporting files.
10. After helper changes or switching projects, restart the kernel and rerun its
    setup cells to avoid stale imports. State the supported working directory.
11. Prefer small manual demonstrations. Add automated tests when they teach or
    meaningfully verify a required behavior.

## Folder structure

```text
<number>_<project_name>/
├── docs/
│   ├── dataset/        # Source documents and question inputs
│   ├── goldends/       # Reference answers, labels, or relevant source IDs
│   ├── evaluatedds/    # Saved application outputs, if needed
│   └── evalresults/    # Saved observations and reports, if needed
├── models/            # Model/store settings and loading functions
├── prompts/           # Instructions used by the application
├── tools/             # Preparation and reusable application helpers
├── readme.md
└── <project>.ipynb
```

Keep the existing `goldends` spelling. Empty directories can use `.gitkeep`.
Add other files or folders when needed; the structure does not require extra
abstraction layers. Keep one project README explaining the goal, input/output,
data provenance, folder responsibilities, setup, and notebook flow. The root
README stays short, with shared setup and a one-line introduction to each lesson.

## Data, preparation, and comparisons

- Preserve reference material and source data. Use fictional examples for the
  teaching projects.
- Prepare and index documents explicitly, separately from request execution.
  Project 3 runs preparation with `uv run python -m tools.prepare_data` from its
  numbered folder. Reuse the existing index for subsequent questions.
- Define shared model and store settings once. Use module-relative paths rather
  than a particular machine's checkout path.
- Keep stable case and source IDs. AI-drafted references remain drafts until
  reviewed by the learner. Keep reference answers out of the index and prompts.
- Inspect an answer and its source evidence, explore one information gap, change
  one variable, and compare the same input. Save previous results and record the
  settings. A useful experiment can show a worse result or an inconclusive gain.
- Label intentional failures and simulated conditions. Do not invent model
  outputs, timings, token counts, human judgments, or trace links.
- Distinguish execution status from answer quality. An honest acknowledgment of
  missing information can be a correct answer.

## Credentials and publishing

Keep credentials in the ignored root `.env`; `.env.example` contains
placeholders. Exclude environments, model caches, generated vector stores,
notebook checkpoints, and private settings from Git. Review notebook outputs
for credentials and local paths before publishing. Preserve useful lesson
results after removing private information.

See [observability-roadmap.md](observability-roadmap.md) for the lesson sequence.
