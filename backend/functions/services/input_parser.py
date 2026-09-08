from dataclasses import dataclass
import re
from urllib.parse import urlparse


URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
TRAILING_URL_PUNCTUATION = ".,;:!?)]}>'\""


@dataclass(frozen=True)
class ParsedMessage:
    """The user text separated from any URLs embedded in it."""

    message: str
    urls: list[str]


@dataclass(frozen=True)
class GitHubRepository:
    """A validated GitHub repository identifier."""

    owner: str
    repo: str
    url: str


def extract_urls(text: str) -> list[str]:
    """Return unique HTTP(S) URLs in message order."""
    urls: list[str] = []

    for match in URL_PATTERN.finditer(text):
        url = match.group(0).rstrip(TRAILING_URL_PUNCTUATION)
        if url and url not in urls:
            urls.append(url)

    return urls


def split_message_and_urls(text):
    if not isinstance(text, str):
        raise ValueError("The message must be text.")

    urls = extract_urls(text)
    message = URL_PATTERN.sub(" ", text)
    message = " ".join(message.split())

    return ParsedMessage(message=message, urls=urls)


def parse_github_repository_url(url: str) -> GitHubRepository:
    """Validate a GitHub repository URL and return its owner and repository name."""
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("The source link must use http or https.")

    if parsed.hostname not in {"github.com", "www.github.com"}:
        raise ValueError("Only GitHub repository links are supported right now.")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise ValueError(
            "The GitHub link must include both an owner and repository, for example "
            "https://github.com/owner/repository."
        )

    owner = parts[0]
    repo = parts[1][:-4] if parts[1].endswith(".git") else parts[1] # check if the repo end with ".git"

    if not owner or not repo:
        raise ValueError(
            "The GitHub link must include both an owner and repository, for example "
            "https://github.com/owner/repository."
        )

    return GitHubRepository(owner=owner, repo=repo, url=url)
