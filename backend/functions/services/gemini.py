from google import genai
from services.repository_prompt import REPOSITORY_REVIEW_PROMPT
from config import GEMINI_API_KEY


def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please set it in the .env file.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def create_prompt(data):

    return REPOSITORY_REVIEW_PROMPT.format(
        owner=data["owner"],
        repo=data["repo"],
        description=data["description"],
        language=data["language"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        readme_content=data["readme"],
        last_commits=data["commits"],
        commit_changes=data["changes"]
    )
