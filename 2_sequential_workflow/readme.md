# Project 2 — Sequential workflow

## Goal

See how `@traceable` records ordinary Python functions, how two dependent model
steps appear as runs inside one request trace, and how metadata makes that trace
easy to find in LangSmith.

## Data and flow

The inputs are fictional. `docs/dataset/job_description.txt` describes a Cedar
Health analyst role. `docs/dataset/candidate_profile.txt` contains Maya's
experience. The first step extracts requirements from the job description. The
second step uses those requirements and Maya's profile to draft a short cover
letter:

```text
job description -> extract_requirements -> requirements
                                             + candidate profile
                                             -> write_cover_letter -> letter
```

The files in `prompts/` hold the two instructions sent to the model.
`models/llm.py` creates the Groq model. `tools/workflow.py` defines the two
steps and the parent `create_cover_letter` function. All three functions use
`@traceable`. The notebook displays the source inputs, intermediate
requirements, and final letter.

## Run the notebook

Complete the [shared setup](../README.md#setup). Use the shared
`learning-observability/.venv` kernel in VS Code and run
`sequential_workflow.ipynb` with `2_sequential_workflow` as its working
directory. The repository root `.env` needs your API keys,
`LANGSMITH_TRACING=true`, `LANGSMITH_AGENT_ID=sequential-workflow`, and
`LANGSMITH_AGENT_ENVIRONMENT=local`. Do not put keys in the notebook.

The two standalone function calls show each step's output. The final notebook
call invokes `create_cover_letter` once, making two model calls inside one
trace. Its metadata includes `case_id=cedar-health-001`, `prompt_version=v1`,
and `lesson=sequential-workflow`.

In LangSmith, open **sequential-workflow → Local → Tracing** and find that case
ID in the trace metadata. Open the `cover_letter_request` parent run and expand
the run tree to see the parent request, the
two traced functions, and a model call under each function. The requirements
returned by the first step are passed to the second step before the letter is
written. A trace shows this execution path; it does not by itself grade the
quality of the letter.

Restart the kernel after editing imported helpers or switching lessons. The
notebook saves example outputs; the fictional profile and job description are
the application's inputs, and this tracing lesson has no labelled evaluation
dataset or scoring suite.

## Folder structure

```text
2_sequential_workflow/
├── docs/
│   ├── dataset/
│   │   ├── job_description.txt
│   │   └── candidate_profile.txt
│   ├── goldends/           # Reserved for reference answers
│   ├── evaluatedds/        # Reserved for saved outputs
│   └── evalresults/        # Reserved for reports
├── models/llm.py           # Groq model loader
├── prompts/
│   ├── requirements.txt
│   └── cover_letter.txt
├── tools/workflow.py       # Two steps and the traced parent request
├── sequential_workflow.ipynb
└── readme.md
```
