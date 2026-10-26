from pathlib import Path

from langsmith import traceable

from models.llm import get_model


project_dir = Path(__file__).resolve().parents[1]


@traceable(name="extract_requirements")
def extract_requirements(job_description):
    template = (project_dir / "prompts" / "requirements.txt").read_text(
        encoding="utf-8"
    )
    prompt = template.format(job_description=job_description)
    return get_model().invoke(prompt).content


@traceable(name="write_cover_letter")
def write_cover_letter(requirements, candidate_profile):
    template = (project_dir / "prompts" / "cover_letter.txt").read_text(
        encoding="utf-8"
    )
    prompt = template.format(
        requirements=requirements,
        candidate_profile=candidate_profile,
    )
    return get_model().invoke(prompt).content


@traceable(name="cover_letter_request")
def create_cover_letter(job_description, candidate_profile):
    requirements = extract_requirements(job_description)
    letter = write_cover_letter(requirements, candidate_profile)
    return {
        "requirements": requirements,
        "letter": letter,
    }
