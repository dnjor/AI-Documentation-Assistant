from config import GITHUB_TOKEN
import requests
from urllib.parse import urlparse
import base64


BASE_URL = "https://api.github.com"


def extract_repo(url):
    if not url:
        raise Exception("URL is empty")

    parsed = urlparse(url)

    if parsed.netloc != "github.com":     # Check if the URL is a GitHub URL, because user might provide a different URL
        raise Exception("Not a GitHub URL")

    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise Exception("Invalid GitHub URL. It should be in the format: https://github.com/owner/repo")

    owner = parts[0] # The first part of the path is the owner of the repository
    repo = parts[1].replace(".git", "") # The second part of the path is the name of the repository, removing the .git suffix if present

    return owner, repo


def github_request(endpoint):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(response.json())

    return response.json()


def get_repo_info(url):
    owner, repo = extract_repo(url)
    endpoint = f"/repos/{owner}/{repo}"
    return github_request(endpoint)


def get_repo_readme(url):
    owner, repo = extract_repo(url)
    endpoint = f"/repos/{owner}/{repo}/readme"
    response = github_request(endpoint)

    content = response["content"]

    decoded_content = base64.b64decode(content).decode("utf-8")

    return decoded_content


def get_repo_file_content(url, file_path):
    owner, repo = extract_repo(url)
    endpoint = f"/repos/{owner}/{repo}/contents/{file_path}"
    return github_request(endpoint)


def get_repo_commits(url):
    owner, repo = extract_repo(url)
    endpoint = f"/repos/{owner}/{repo}/commits"
    return github_request(endpoint)


def get_repo_commits_changes(url, commit_sha):
    owner, repo = extract_repo(url)
    endpoint = f"/repos/{owner}/{repo}/commits/{commit_sha}"
    return github_request(endpoint)
