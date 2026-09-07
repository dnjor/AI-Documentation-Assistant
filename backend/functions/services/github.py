from config import GITHUB_TOKEN
import requests
from urllib.parse import urlparse

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
