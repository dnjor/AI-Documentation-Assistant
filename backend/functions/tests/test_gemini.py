from unittest.mock import MagicMock

import pytest

from services import gemini


@pytest.fixture
def valid_repository_data():
    return {
        "user_request": "Review the setup documentation for new developers.",
        "owner": "acme",
        "repo": "docs-app",
        "description": "Example documentation project",
        "language": "Python",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "readme": "# Docs App\n\nInstall with pip.",
        "commits": [],
        "changes": [],
    }


class TestAskGemini:
    def test_returns_text_from_valid_gemini_response(self, monkeypatch):
        fake_response = MagicMock()
        fake_response.text = "Documentation needs an installation section." # fake response text from Gemini API

        fake_client = MagicMock()
        fake_client.models.generate_content.return_value = fake_response
        fake_client_class = MagicMock(return_value=fake_client)

        monkeypatch.setattr(gemini, "GEMINI_API_KEY", "test-api-key") # fake API key for testing
        monkeypatch.setattr(gemini.genai, "Client", fake_client_class)

        result = gemini.ask_gemini("Review this README.")

        assert isinstance(result, str)
        assert result == "Documentation needs an installation section."
        fake_client_class.assert_called_once_with(api_key="test-api-key")
        fake_client.models.generate_content.assert_called_once_with(
            model="gemini-3.6-flash",
            contents="Review this README.",
        )

    def test_rejects_missing_api_key(self, monkeypatch):
        monkeypatch.setattr(gemini, "GEMINI_API_KEY", None)

        with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
            gemini.ask_gemini("Review this README.")


class TestCreatePrompt:
    def test_creates_text_prompt_from_valid_repository_data(self, valid_repository_data):
        prompt = gemini.create_prompt(valid_repository_data)

        assert isinstance(prompt, str)
        assert valid_repository_data["user_request"] in prompt
        assert "Owner:\nacme" in prompt
        assert "Repository Name:\ndocs-app" in prompt
        assert valid_repository_data["readme"] in prompt

    def test_rejects_missing_required_prompt_value(self, valid_repository_data):
        valid_repository_data.pop("repo")

        with pytest.raises(KeyError):
            gemini.create_prompt(valid_repository_data)
