from models.vector_store import PROJECT_ROOT, load_vector_store
from dotenv import load_dotenv
from langsmith import Client, agent_address, traceable


load_dotenv(PROJECT_ROOT.parent / ".env")

client = Client()
TRACE_ADDRESS = agent_address("rag-tracing", "local")


@traceable(client=client, address=TRACE_ADDRESS)
def load_policy_sections():
    sections = []
    dataset_dir = PROJECT_ROOT / "docs" / "dataset"

    for policy_path in sorted(dataset_dir.glob("*_policy.md")):
        text = policy_path.read_text(encoding="utf-8")

        for section in text.split("\n## ")[1:]:
            section_id = section.split(":", 1)[0].strip()

            sections.append(
                {
                    "section_id": section_id,
                    "source": policy_path.name,
                    "text": section.strip(),
                }
            )

    return sections


@traceable(client=client, address=TRACE_ADDRESS)
def prepare_vector_store():
    sections = load_policy_sections()
    assert sections, "No policy sections were found."

    vector_store = load_vector_store(create=True)

    vector_store.add_texts(
        texts=[section["text"] for section in sections],
        metadatas=[
            {
                "section_id": section["section_id"],
                "source": section["source"],
            }
            for section in sections
        ],
        ids=[section["section_id"] for section in sections],
    )

    return len(sections)


if __name__ == "__main__":
    count = prepare_vector_store()
    client.flush()
    print(f"Policy sections indexed: {count}")
