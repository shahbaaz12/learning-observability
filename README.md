# Learning observability

Small notebook projects for learning how LangSmith records an LLM application's
execution. Each numbered folder is a separate lesson; all lessons use the same
root Python environment.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and VS Code
with the Python and Jupyter extensions. Then run in PowerShell:

```powershell
git clone https://github.com/shahbaaz12/learning-observability.git
cd learning-observability
uv sync
Copy-Item .env.example .env
```

Add your Groq and LangSmith API keys to `.env`. Keep `LANGSMITH_TRACING=true`
and use the lesson's agent ID with the `local` environment, as explained in its
README. `.env` is private and ignored by Git.

Open a lesson's `.ipynb` file in VS Code, select the repository's
`.venv/Scripts/python.exe` kernel, and use its numbered folder as the working
directory. All lessons share the root environment. Project 3's README includes
its separate data-preparation command.

## Lessons

1. [Basic tracing](1_basic_tracing/readme.md) — inspect one model request and an intentional input-validation error.
2. [Sequential workflow](2_sequential_workflow/readme.md) — follow two dependent model calls inside a cover-letter request.
3. [RAG tracing](3_rag_tracing/readme.md) — follow policy evidence into an answer and investigate missing information or context.

Each project README explains its data, folder structure, setup, and notebook
flow. See [rule.md](rule.md) for the learning workflow and the
[roadmap](observability-roadmap.md) for later lessons.
