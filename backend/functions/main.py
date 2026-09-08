import json

from firebase_functions import https_fn
from firebase_admin import initialize_app

from services.assistant_prompt import create_conversation_prompt
from services.gemini import ask_gemini, create_prompt
from services.github import get_repo_info, get_repo_readme, get_repo_commits, get_repo_commits_changes
from services.input_parser import split_message_and_urls

initialize_app()


@https_fn.on_request()
def ask_ai(request: https_fn.Request):
    """Handle a documentation chat message with an optional GitHub link."""
    if request.method == "POST":
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            return json_response(
                {"error": "POST requests must use a JSON body containing a message."},
                status=400,
            )
        raw_message = body.get("message")
    elif request.method == "GET":
        # Temporary browser-friendly interface for testing before the frontend
        # exists. The production frontend should use POST.
        raw_message = request.args.get("message")
    else:
        return json_response(
            {"error": "Use GET with ?message=... or POST with a JSON message body."},
            status=405,
        )

    if not isinstance(raw_message, str) or not raw_message.strip():
        return json_response({"error": "Missing message."}, status=400)

    try:
        parsed_message = split_message_and_urls(raw_message)
    except ValueError as error:
        return json_response({"error": str(error)}, status=400)

    if not parsed_message.urls:
        try:
            answer = ask_gemini(create_conversation_prompt(parsed_message.message))
        except Exception:
            return json_response(
                {"error": "I could not respond right now. Please try again."},
                status=502,
            )
        return json_response({"mode": "conversation", "answer": answer})

    if len(parsed_message.urls) > 1:
        return json_response(
            {"error": "Please send one GitHub repository link per message."},
            status=400,
        )

    if not parsed_message.message:
        return json_response(
            {
                "mode": "needs_request",
                "answer": "What would you like me to review or create from this repository?",
            }
        )

    return analyze_repository(parsed_message.urls[0], parsed_message.message)


def analyze_repository(url, user_request):
    try:
        repo_info = get_repo_info(url)
        readme_content = get_repo_readme(url)
        commits = get_repo_commits(url)
    except ValueError as error:
        return json_response({"error": str(error)}, status=400)
    except Exception:
        # Do not expose GitHub API details or credentials to callers.
        return json_response(
            {"error": "I could not access that repository. Check that the link is valid and accessible."},
            status=422,
        )

    for commit in commits[:5]:
        commit_sha = commit["sha"]

        try:
            commit_changes = get_repo_commits_changes(url, commit_sha)
        except Exception:
            # A partial review is preferable to failing after the repository
            # metadata and README have already been fetched.
            commit_changes = {"files": []}

        commit["changes"] = [
            {
                "filename": file["filename"],
                "status": file["status"]
            }
            for file in commit_changes.get("files", [])
        ]

    # Create the prompt for the AI
    prompt = create_prompt({
        "user_request": user_request,
        "owner": repo_info["owner"]["login"],
        "repo": repo_info["name"],
        "description": repo_info["description"],
        "language": repo_info["language"],
        "created_at": repo_info["created_at"],
        "updated_at": repo_info["updated_at"],
        "readme": readme_content[:12000],  # Limit to the first 12000 characters for brevity,
        "commits": commits[:5],  # Limit to the first 5 commits for brevity
        "changes": [commit["changes"] for commit in commits[:5]]  # Limit to the first 5 commits for brevity
    })

    try:
        answer = ask_gemini(prompt)
    except Exception:
        return json_response(
            {"error": "I could not complete the documentation analysis right now."},
            status=502,
        )

    return json_response({"mode": "repository_analysis", "answer": answer})


def json_response(payload, status=200):
    return https_fn.Response(
        json.dumps(payload),
        status=status,
        content_type="application/json",
    )
