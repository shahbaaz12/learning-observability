# Observability learning roadmap

This is the portable repository guide. Follow [rule.md](rule.md) and the active
project's `readme.md`. Teach one explained snippet at a time and continue when
the learner says `next` or equivalent.

Status on 26 October 2026: Projects 1 and 2 were completed by the learner.
Project 3's core flow, saved examples, and learning notes are complete. Human
review of its draft reference answers remains pending. Later folders are
created only when the learner starts those lessons.

## Shared approach

1. Explain the learning goal and the smallest working result.
2. Show setup commands and the standard numbered-folder structure.
3. Explain each helper, then provide one small implementation snippet.
4. Give a manual command or cell and its expected visible result.
5. Wait for `next`; inspect or test when requested with `-check`, or as required
   for an explicitly requested edit or review.
6. Inspect evidence, explore a problem, change one variable, and compare.
7. Record actual observations in notebook Markdown and the project README.
8. Let the learner choose whether to start another project.

Use the shared root uv environment and VS Code notebooks. Keep preparation,
model/store setup, and reusable logic in supporting files. New HR lessons reuse
the fictional policy data and stable IDs from Project 3 in their own folders,
with explicit preparation; avoid imports through sibling numbered projects.

## 1. Basic tracing

Folder: `1_basic_tracing`. Goal: explain one successful request and one error.

1. Configure the shared environment and `basic-tracing` agent's Local environment.
2. Read the fictional greeting prompt and make one direct model call.
3. Add a small traced request function with nonempty-input validation.
4. Inspect the successful request's input, output, duration, and nested model run.
5. Run blank input in a separate cell and inspect the intentional validation error.
6. Explain what execution success and failure do, and do not, establish about quality.

## 2. Sequential workflow

Folder: `2_sequential_workflow`. Goal: follow an intermediate result across two calls.

1. Read the fictional job description and candidate profile.
2. Extract job requirements and display the result.
3. Generate a cover letter using those requirements and the candidate profile.
4. Trace both functions and connect them in one parent request.
5. Add case ID, prompt version, and lesson metadata to the combined call.
6. Inspect the nested runs, intermediate handoff, and metadata in LangSmith.

## 3. RAG tracing

Folder: `3_rag_tracing`. Goal: connect an answer to the evidence supplied to the model.

1. Prepare three fictional policies and a six-question set with separate draft references.
2. Preserve source IDs and keep goldens separate from application inputs.
3. Define the local Chroma store and embedding model in `models/vector_store.py`.
4. Read, embed, save, and trace policy sections through `tools/prepare_data.py`.
5. Open the index once, retrieve sections, and inspect their text and IDs.
6. Format context, build the prompt, and make one direct model call.
7. Connect retrieval, formatting, and generation under an `answer_question` trace.
8. Ask an unsupported sick-leave question and inspect the acknowledgment of missing information.
9. Omit context for the supported annual-leave question and compare the same question again.
10. Preserve actual observations and a learning recap in the notebook and README.

The core notebook has seven code cells with saved outputs. The learner confirmed
trace visibility. Trace links and separate reports have not been recorded.

## 4. Latency debugging — planned

Folder: `4_latency_debugging`. Goal: identify repeated setup work and measure one change.

1. Create the standard folder layout and reuse the working fictional HR example.
2. Prepare the index once and define startup versus request timing boundaries.
3. Build a labelled baseline that loads the embedding model and opens the saved
   store inside each request; keep indexing outside request execution.
4. Inspect a trace and identify where time is spent.
5. Load resources once outside requests and reuse the same answering logic.
6. Compare the same question in three paired baseline/candidate runs, recording
   startup and request timings separately along with answer evidence.
7. Save the results and explain the observed gain, trade-off, or inconclusive outcome.

## 5. Token and cost debugging — planned

Folder: `5_token_and_cost_debugging`. Goal: understand usage and its quality trade-offs.

1. Choose fixed reviewed questions, including one requiring two policy sections.
2. Run the RAG app with three retrieved sections and inspect model input/output usage.
3. Change only retrieval `k` from 3 to 1 and repeat the same questions.
4. Compare supplied evidence, token counts, and answer quality.
5. Estimate cost only when applicable provider prices are available; record the
   price source, date, currency, units, and assumptions.
6. Use parent totals or model-call leaf totals consistently to avoid double counting.
7. Save baseline and candidate results. Keep missing usage or cost marked unavailable.

## 6. Monitoring and feedback — planned

Folder: `6_monitoring_and_feedback`. Goal: connect a pattern across requests to its cause.

1. Label a bounded workload of the six policy questions with case and batch IDs.
2. Run the valid-input questions, then one intentional blank-input error separately.
3. Select the matching root request runs, excluding preparation, children, and
   earlier experiments from the request count.
4. Summarize request count, failures, average latency, and available usage/cost.
5. Have the learner rate actual answers with a simple useful/not-useful rubric
   and attach genuine feedback to the relevant run IDs.
6. Choose one observed metric and a learning threshold; flag a request or batch.
7. Inspect the associated trace, change one cause, and repeat the same cases.
8. Save the comparison. Show each metric's scope and denominator, including the
   number of human-reviewed answers. Label intentional failures.
9. Optionally explore hosted dashboards and one alert after the notebook works,
   depending on account access and the learner's choice.

## 7. Local tool-call tracing — optional

Folder: `7_tool_call_tracing`. Goal: follow one bounded tool interaction.

1. Add two simple local policy tools and call each directly.
2. Inspect one model-proposed tool call and its arguments.
3. Execute at most one tool and pass its result into the final model call.
4. Inspect selection, arguments, returned evidence, and the final answer in a trace.
5. Demonstrate an invalid section ID separately, correct it, and compare.

## 8. LangGraph tracing — optional

Folder: `8_langgraph_tracing`. Goal: inspect a small branch and its state transitions.

1. Add LangGraph only when starting this lesson.
2. Draw a graph that routes a policy question to an answer or an unsupported-topic message.
3. Define minimal state and ordinary node functions, then connect the graph.
4. Inspect one supported route and one unsupported route in their traces.
5. Correct a labelled routing problem and compare the same question.
6. Treat parallel execution and persistence as later extensions.

## Handoff and references

Read the active project's README progress section before continuing. Record
the last confirmed step, actual result, saved evidence, and next single step.
Do not rerun paid calls merely to recover saved state. Current next lesson:
Project 4, when the learner chooses to begin.

Reference examples: [campusx-official/langsmith-masterclass](https://github.com/campusx-official/langsmith-masterclass).
Use current official documentation for SDK syntax and service features when a
lesson starts. Original source notes are not included in this repository;
credentials stay in the ignored root `.env`.
