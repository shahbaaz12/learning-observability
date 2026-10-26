# Project 3 — RAG tracing

## Goal

Build a small application that answers questions using fictional HR policies,
then use LangSmith to follow the evidence from retrieval to the final answer.

RAG means retrieval-augmented generation: find relevant information first,
then give that information to the model with the question.

Project 1 showed a single request. Project 2 connected two dependent model
steps. This project adds retrieval and makes the context sent to the model
visible.

We want to answer three questions:

1. Which policy sections did the retriever return?
2. What context did the model actually receive?
3. Does the answer use the facts in that context?

A trace helps locate missing evidence or an incorrect handoff. Comparing the
answer with the policy establishes whether the answer is supported.

## Example and flow

Example question: **How many days of annual leave does the policy allow?**

The app should find the relevant fictional leave-policy section and answer
using that section, including its source ID. If the supplied policies do not
contain an answer, it should say so.

```text
Preparation, run separately:
policy documents -> sections with IDs -> embeddings -> saved local index

Answering a question:
question -> retrieve sections -> build context -> model -> answer + source IDs
```

Preparation has its own trace. Each complete question request connects
retrieval, context preparation, and the model call inside one parent trace.
Questions reuse the prepared index.

## Folder structure

```text
3_rag_tracing/
├── docs/
│   ├── dataset/        # Fictional policy documents and prepared sections
│   ├── goldends/       # Draft reference answers and relevant source IDs
│   ├── evaluatedds/    # Saved answers, if needed
│   └── evalresults/    # Saved observations and comparisons, if needed
├── models/
│   ├── llm.py          # Groq model settings and loader
│   └── vector_store.py # Embedding model and saved Chroma collection
├── prompts/
│   └── rag_answer.txt  # Answering instructions and context/question placeholders
├── tools/
│   ├── prepare_data.py # Read, embed, index, and trace policy preparation
│   └── rag.py          # Retrieve sections, format context, and answer questions
├── readme.md
└── rag_tracing.ipynb    # Short calls, visible results, and trace observations
```

The `.gitkeep` files preserve currently empty directories in Git; they are not
lesson data. `tools/prepare_data.py` reads and indexes the policy sections.
The generated `chroma_store/` will be ignored by the existing repository rules.

## Shared setup

Use the existing `learning-observability` environment. If it needs syncing,
run this command from the repository root after the [shared setup](../README.md#setup):

```powershell
uv sync
```

Open `rag_tracing.ipynb` in VS Code. Select
`learning-observability/.venv/Scripts/python.exe` as its kernel and use
`3_rag_tracing` as the notebook's working directory.

Keep keys in the repository root `.env`, as in Projects 1 and 2, with
`LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, and `GROQ_API_KEY` configured.
Both the preparation script and notebook load that file. Project 3 explicitly
routes traces with `agent_address("rag-tracing", "local")`, which takes
precedence over a previous lesson's default agent settings.

The answer model is `openai/gpt-oss-20b`, hosted by Groq. The local embedding
model is `BAAI/bge-small-en-v1.5`, running on CPU. Chroma stores the
`cedar_health_hr_v1` collection using cosine distance. These choices are defined
in `models/`; the notebook imports their loaders.

## Run preparation

From PowerShell at the repository root, run:

```powershell
cd 3_rag_tracing
uv run python -m tools.prepare_data
```

Expected terminal output: `Policy sections indexed: 6`.

Both preparation functions use `@traceable`. In LangSmith, open
**rag-tracing → Local → Tracing** and expand the preparation trace:

```text
prepare_vector_store
└── load_policy_sections
```

The child returns the policy text, section IDs, and filenames. The parent
duration includes loading, embedding-model setup, embedding, and storage.
`client.flush()` waits for pending traces before the script exits. The prepared
index is saved in this project's `chroma_store/` directory.

Run preparation when creating or deliberately updating the index. A change to
retrieval `k` alone uses the same stored sections. Review reference source IDs
if the section boundaries or IDs change.

## Data

Dataset version: `cedar-health-hr-v1`. All policy facts are fictional.

| File | Contents |
| --- | --- |
| `docs/dataset/leave_policy.md` | Annual leave entitlement and how to request leave; sections `LEAVE-001` and `LEAVE-002` |
| `docs/dataset/notice_policy.md` | Notice period and resignation procedure; sections `NOTICE-001` and `NOTICE-002` |
| `docs/dataset/payroll_policy.md` | Salary payment date and payslip guidance; sections `PAYROLL-001` and `PAYROLL-002` |
| `docs/dataset/questions.json` | Six question inputs with stable `case_id` values |
| `docs/goldends/reference_answers.json` | Draft expected answers, answerability, and relevant section IDs for the same cases |

The question set contains four direct questions, one requiring both the leave
and notice policies, and one asking about sick leave, which these policies do
not specify. For that last case, the expected behavior is to acknowledge the
missing information rather than invent an entitlement.

Match a question to its reference answer using `case_id`. Both JSON files are
simple lists of records. Reference wording is an example of the required facts;
we will inspect meaning and evidence rather than require an exact text match.

The learner added the leave policy from the earlier supplied snippet. The
assistant added the other two fictional policies, questions, and reference
answers at the learner's request. All reference answers have
`review_status: "draft"`; human review is still pending.

During preparation, index only the `*_policy.md` files. Each `##` section starts
with a stable source ID. Keep those IDs in the prepared sections and retrieval
results. Questions and reference answers must stay out of the index and the
retrieved context. Send the current question to the app, then use the references
separately to inspect its output.

## Notebook flow

The notebook now contains seven code cells, each preceded by explanatory
Markdown, followed by saved observations and a learning recap.

| Step | What happens | What to inspect |
| --- | --- | --- |
| 1. Retrieve evidence | Load environment settings, open the saved index, and search with `k=3` | Policy text, section IDs, and filenames |
| 2. Format context | Combine retrieved documents into a readable string | Evidence retained in the formatted text |
| 3. Build the prompt | Fill the template's context and question placeholders | Complete instructions and evidence supplied to the model |
| 4. Generate directly | Make one standalone model call | The model's prompt and response |
| 5. Run the complete request | Call `answer_question()` | One parent trace with retrieval, formatting, and model children |
| 6. Ask about sick leave | Run a question the policies do not answer | Whether the response acknowledges the information gap |
| 7. Remove context | Send the original annual-leave question with empty context | How the same model responds when the evidence is omitted |

Steps 4–7 each make a model call when executed. The complete-request cell
reuses the application's helper functions. Preparation remains a separate
terminal command.

Keep notebook cells short. Explain each helper before importing it. Use ordinary
functions without `try`/`except` or extra application layers. After editing an
imported helper, restart the kernel and rerun the setup cells.

At each step, provide one snippet, its target file, how to run it, and what to
expect. Continue when the learner says `next` or equivalent. Inspect or test
the learner's work only when requested with `-check`.

## Read the request trace

Open **rag-tracing → Local → Tracing** in LangSmith. Select the agent and
environment for this lesson, then expand `answer_question`:

```text
answer_question
├── retrieve_sections
├── format_context
└── ChatGroq
```

`@traceable` records a function's inputs, outputs, duration, and status.
`run_type="retriever"` identifies the search step. Calls between decorated
functions establish the hierarchy, and the Groq integration records the
model call automatically.

Follow the section IDs through the retrieval output, context output, model
input, and answer citations. The parent duration covers the request; loading
the vector store and building the index happen outside that timing boundary.

The `missing_context_demo` diagnostic is a direct model call with an empty
policy context. Its trace shows the model input and answer for that experiment.
Use it to compare answer behavior with the supported example; a model-only
duration and a whole-request duration measure different operations.

## Saved observations

These observations come from the outputs already saved in `rag_tracing.ipynb`.
They were preserved during the documentation update on 24 October 2026.

| Case | Saved result | Learning |
| --- | --- | --- |
| Annual-leave question with retrieved context | 18 days per calendar year, with `[LEAVE-001]` | A policy fact can be followed from evidence to answer |
| Paid sick-leave question | The supplied policies do not specify the number of days | Similar retrieved text can still lack the requested fact |
| Annual-leave question with empty context | The supplied policies do not specify the entitlement | Removing evidence changes the response to the same question |

The learner confirmed that the new lesson's traces are visible in LangSmith.
Trace URLs and exported result reports have not been recorded. The six-case
JSON question set is available for later use; the notebook's three examples
are teaching demonstrations rather than a full evaluation of that set.

## What we learned

1. **Prepare once, then reuse the index.** Policy loading and indexing have a
   separate lifecycle from answering individual questions.
2. **Inspect retrieved text.** Similarity search finds nearby sections;
   inspecting their content establishes whether the needed fact is present.
3. **Preserve source IDs.** They connect retrieved sections, context, and
   citations, making answers easier to investigate.
4. **Inspect the actual model input.** A correct fact in a source file helps
   only when the relevant evidence reaches the assembled prompt.
5. **Distinguish two information gaps.** Sick-leave information is absent from
   the source documents. Annual-leave information exists, but the diagnostic
   deliberately omits it from the model's input.
6. **Separate execution status from answer quality.** An honest acknowledgment
   of missing information can be a successful answer. A success status alone
   does not establish correctness.
7. **Use consistent trace scope.** Individual model calls, complete requests,
   and preparation runs cover different operations and timings.

The smallest working learning loop is present: inspect a supported answer,
explore an information gap, change only the supplied context, and compare the
same question again. Reading the underlying policy remains part of judging
whether a citation supports the answer.

## Progress

- Status: core Project 3 flow and learning notes complete; reference answers await human review.
- Previous lessons: Projects 1 and 2 completed, as reported by the learner.
- Current milestone: complete RAG trace, unsupported question, and empty-context comparison are implemented and have saved notebook outputs.
- Data files: three policy documents, `questions.json`, and `reference_answers.json`.
- Documentation updated: 24 October 2026. Existing code cells, execution counts, outputs, and notebook metadata were preserved; the edit made no model calls or indexing runs.
- Dataset version: `cedar-health-hr-v1`; embedding model: `BAAI/bge-small-en-v1.5`; answer model: `openai/gpt-oss-20b`; prompt: `prompts/rag_answer.txt`.
- Evidence: saved notebook outputs and learner-confirmed trace visibility; trace links and separate reports remain unrecorded.
- Next single step: review the learning notes; discuss Project 4, latency debugging, when the learner chooses to continue.
- Pending review: draft reference answers require human review before use as trusted goldens.

Guidance: [learning rules](../rule.md) and
[observability roadmap](../observability-roadmap.md).
