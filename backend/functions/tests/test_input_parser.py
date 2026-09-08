import pytest
from services.input_parser import extract_urls, parse_github_repository_url, split_message_and_urls

class TestInputParserExtractUrls:
    def test_extract_urls_returns_correct_url(self):
        text = "can you check my repo https://github.com/user/repo"
        urls = extract_urls(text)
        assert urls[0] == "https://github.com/user/repo"

    def test_extract_urls_missing_url(self):
        text = "can you check my repo"
        urls = extract_urls(text)
        with pytest.raises(IndexError):
            _ = urls[0]

    def test_extract_urls_multiple_urls(self):
        text = "can you check my repo https://github.com/user/repo1 and https://gitlab.com/user/repo2"
        urls = extract_urls(text)
        assert urls[0] == "https://github.com/user/repo1"
        assert urls[1] == "https://gitlab.com/user/repo2"

    def test_extract_urls_with_type_error(self):
        text = 12345  # Not a string
        with pytest.raises(TypeError):
            extract_urls(text)

class TestInputParserSplitMessageAndUrls:
    def test_split_message_and_urls_returns_correct_parsed_message(self):
        text = "can you check my repo https://github.com/user/repo1"
        result = split_message_and_urls(text)
        assert result.message == "can you check my repo"
        assert result.urls[0] == "https://github.com/user/repo1"

    def test_split_message_and_urls_missing_url(self):
        text = "can you check my repo"
        result = split_message_and_urls(text)
        assert result.message == "can you check my repo"
        assert result.urls == []

    def test_split_message_and_urls_multiple_urls(self):
        text = "can you check my repo https://github.com/user/repo1 and https://gitlab.com/user/repo2"
        result = split_message_and_urls(text)
        assert result.message == "can you check my repo and"
        assert result.urls[0] == "https://github.com/user/repo1"
        assert result.urls[1] == "https://gitlab.com/user/repo2"

    def test_split_message_and_urls_with_value_error(self):
        text = 12345  # Not a string
        with pytest.raises(ValueError):
            split_message_and_urls(text)


class TestInputParserParseGitHubRepositoryUrl:
    def test_parse_github_repository_url_valid_url(self):
        url = "https://github.com/user/repo"
        result = parse_github_repository_url(url)
        assert result.owner == "user"
        assert result.repo == "repo"
        assert result.url == url

    def test_parse_github_repository_url_valid_url_with_https_scheme(self):
        url1 = "https://github.com/user/repo"
        result1 = parse_github_repository_url(url1)
        assert result1.url == url1

        url2 = "http://github.com/user/repo"
        result2 = parse_github_repository_url(url2)
        assert result2.url == url2

    def test_parse_github_repository_url_valid_url_with_different_hostname(self):
        url1 = "https://www.github.com/user/repo"
        result1 = parse_github_repository_url(url1)
        assert result1.url == url1

        url2 = "https://github.com/user/repo"
        result2 = parse_github_repository_url(url2)
        assert result2.url == url2

    def test_parse_github_repository_url_invalid_scheme(self):
        url = "ftp://github.com/user/repo"
        with pytest.raises(ValueError):
            parse_github_repository_url(url)

    def test_parse_github_repository_url_invalid_hostname(self):
        url = "https://gitlab.com/user/repo"
        with pytest.raises(ValueError):
            parse_github_repository_url(url)

    def test_parse_github_repository_url_missing_owner(self):
        url = "https://github.com//repo"
        with pytest.raises(ValueError):
            parse_github_repository_url(url)

    def test_parse_github_repository_url_missing_repo(self):
        url = "https://github.com/user/"
        with pytest.raises(ValueError):
            parse_github_repository_url(url)
