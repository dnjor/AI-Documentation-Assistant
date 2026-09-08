from firebase_functions import https_fn
from firebase_admin import initialize_app

from services.gemini import ask_gemini, create_prompt
from services.github import get_repo_info, get_repo_readme, get_repo_file_content, get_repo_commits, get_repo_commits_changes

initialize_app()


@https_fn.on_request()
def ask_ai(request: https_fn.Request):

    data = request.args.get("url_repo")

    if not data:
        return https_fn.Response(
            "Missing repository URL",
            status=400
        )

    # Fetch repository information
    repo_info = get_repo_info(data)
    readme_content = get_repo_readme(data)
    commits = get_repo_commits(data)

    commits = get_repo_commits(data)

    for commit in commits[:5]:
        commit_sha = commit["sha"]

        commit_changes = get_repo_commits_changes(
            data,
            commit_sha
        )

        commit["changes"] = [
            {
                "filename": file["filename"],
                "status": file["status"]
            }
            for file in commit_changes.get("files", [])
        ]

    # Create the prompt for the AI
    prompt = create_prompt({
        "owner": repo_info["owner"],
        "repo": repo_info["name"],
        "description": repo_info["description"],
        "language": repo_info["language"],
        "created_at": repo_info["created_at"],
        "updated_at": repo_info["updated_at"],
        "readme": readme_content[:12000],  # Limit to the first 12000 characters for brevity,
        "commits": commits[:5],  # Limit to the first 5 commits for brevity
        "changes": [commit["changes"] for commit in commits[:5]]  # Limit to the first 5 commits for brevity
    })

    answer = ask_gemini(prompt)

    return https_fn.Response(answer)
