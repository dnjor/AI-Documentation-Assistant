from config import GITHUB_TOKEN
import requests
import base64

from services.input_parser import parse_github_repository_url


BASE_URL = "https://api.github.com"


def extract_repo(url):
    repository = parse_github_repository_url(url)
    return repository.owner, repository.repo


def github_request(endpoint):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers,
        timeout=15,
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
