from langsmith import agent_address, traceable


@traceable(
    run_type="retriever",
    address=agent_address("rag-tracing", "local"),
)
def retrieve_sections(question, vector_store, k=3):
    return vector_store.similarity_search(question, k=k)


@traceable(address=agent_address("rag-tracing", "local"))
def format_context(documents):
    return "\n\n".join(
        f"[{document.metadata['section_id']}] "
        f"{document.metadata['source']}\n"
        f"{document.page_content}"
        for document in documents
    )


@traceable(address=agent_address("rag-tracing", "local"))
def answer_question(question, vector_store, llm, prompt_template, k=3):
    assert question.strip(), "Question cannot be empty."

    documents = retrieve_sections(question, vector_store, k=k)
    context = format_context(documents)
    prompt = prompt_template.format(context=context, question=question)
    response = llm.invoke(prompt)

    return response.content
