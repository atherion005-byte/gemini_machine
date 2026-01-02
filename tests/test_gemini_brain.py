import pytest
from types import SimpleNamespace
import os

import gemini_brain


def test_get_viral_script_raises_without_key(monkeypatch):
    # Ensure environment has no key
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    with pytest.raises(RuntimeError):
        gemini_brain.get_viral_script("Test Topic")


def test_get_viral_script_returns_text(monkeypatch, tmp_path):
    # Provide a fake API key and mock the GenerativeModel
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-key')

    class FakeResponse:
        def __init__(self, text):
            self.text = text

    class FakeModel:
        def __init__(self, *args, **kwargs):
            pass

        def generate_content(self, prompt):
            return FakeResponse("*Test Script* #hashtag")

    # Patch the genai import on the module to use a fake model factory
    monkeypatch.setattr(gemini_brain, 'genai', SimpleNamespace(GenerativeModel=lambda name: FakeModel(), configure=lambda api_key: None))

    script = gemini_brain.get_viral_script("Test Topic")
    assert "Test Script" in script
    assert "#" not in script
    assert "*" not in script
