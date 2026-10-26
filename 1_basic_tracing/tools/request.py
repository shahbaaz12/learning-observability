from langsmith import traceable

from models.llm import get_model


@traceable(name="greeting_request")
def greeting_request(prompt):
    assert prompt.strip(), "Prompt must not be empty"
    return get_model().invoke(prompt).content
