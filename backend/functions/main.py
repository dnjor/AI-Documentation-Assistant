from firebase_functions import https_fn
from firebase_admin import initialize_app

from google import genai
from config import GEMINI_API_KEY

initialize_app()

def ask_gemini(question):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please set it in the .env file.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"{question}, please answer in Arabic, and provide a detailed explanation."
    )

    return response.text

@https_fn.on_request()
def ask_ai(request: https_fn.Request):

    question = request.args.get("question")

    if not question:
        return https_fn.Response(
            "Missing question",
            status=400
        )

    answer = ask_gemini(question)

    return https_fn.Response(answer)
