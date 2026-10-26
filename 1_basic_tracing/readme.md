# Project 1 — Basic tracing

## Goal

See what happened during one LLM request and where a failed request stopped.

## Data and code

- `prompts/greeting.txt` contains a fictional greeting request for Maya.
- `models/llm.py` creates the Groq model.
- `tools/request.py` validates the prompt and records the whole request with `@traceable`.
- `basic_tracing.ipynb` runs the examples and records what we observed.

## Run the notebook

Complete the [shared setup](../README.md#setup). In the root `.env`, use
`LANGSMITH_TRACING=true`, `LANGSMITH_AGENT_ID=basic-tracing`, and
`LANGSMITH_AGENT_ENVIRONMENT=local`, alongside your Groq and LangSmith API keys.

Open `basic_tracing.ipynb` with the repository's `.venv` kernel and
`1_basic_tracing` as the working directory. Run the setup and successful-call
cells in order. Run the blank-input cell separately: its `AssertionError` is
intentional, and a top-to-bottom run pauses at that cell.

In **basic-tracing → Local → Tracing**, compare the direct model call, the
successful `greeting_request` trace with its nested model run, and the failed
request with no model run. Restart the kernel after editing imported helpers
or changing lessons.

A trace explains **what happened**. It does not, by itself, prove that an answer is good.

## Folder structure

```text
1_basic_tracing/
├── docs/
│   ├── dataset/        # Reserved for lesson inputs
│   ├── goldends/       # Reserved for reference answers
│   ├── evaluatedds/    # Reserved for saved outputs
│   └── evalresults/    # Reserved for reports
├── models/llm.py       # Shared model-loading function for this lesson
├── prompts/greeting.txt
├── tools/request.py   # Input validation and traced request
├── basic_tracing.ipynb
└── readme.md
```

The four `docs/` subfolders keep the standard project layout. This small lesson
uses its prompt file as input and preserves observations in notebook outputs;
it has no labelled golden dataset or scoring suite.
