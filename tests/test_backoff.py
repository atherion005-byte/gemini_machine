import pytest
from types import SimpleNamespace
import os

import gemini_brain


class FakeResponse:
    def __init__(self, text):
        self.text = text


def test_retry_on_rate_limit_backoff(monkeypatch):
    # Ensure API key present
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-key')

    calls = {'count': 0}
    sleep_calls = []

    # Fake model that raises 429 twice then returns success
    class FakeModel:
        def generate_content(self, prompt):
            calls['count'] += 1
            if calls['count'] <= 2:
                raise Exception('429 Too Many Requests')
            return FakeResponse('*Recovered Script* #tag')

    # Patch genai and time.sleep
    monkeypatch.setattr(gemini_brain, 'genai', SimpleNamespace(GenerativeModel=lambda name: FakeModel(), configure=lambda api_key: None))
    monkeypatch.setattr('time.sleep', lambda s: sleep_calls.append(s))

    script = gemini_brain.get_viral_script('topic', retries=3, backoff_factor=2)

    # Ensure generate_content was called 3 times and sleeps recorded with exponential backoff (5, 10)
    assert calls['count'] == 3
    assert sleep_calls == [5, 10]
    assert 'Recovered Script' in script
    assert '*' not in script and '#' not in script


def test_exhaust_retries_returns_rate_limit_message(monkeypatch):
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-key')

    # Model that always raises 429
    class Always429:
        def generate_content(self, prompt):
            raise Exception('429 Too Many Requests')

    sleep_calls = []
    monkeypatch.setattr(gemini_brain, 'genai', SimpleNamespace(GenerativeModel=lambda name: Always429(), configure=lambda api_key: None))
    monkeypatch.setattr('time.sleep', lambda s: sleep_calls.append(s))

    msg = gemini_brain.get_viral_script('topic', retries=3, backoff_factor=2)
    assert msg == 'System Error. Rate Limit Exceeded.'
    # Should have called sleep `retries` times: 3 sleeps (attempts 0,1,2)
    assert len(sleep_calls) == 3


def test_non_rate_limit_error_returns_refusal(monkeypatch):
    monkeypatch.setenv('GOOGLE_API_KEY', 'fake-key')

    class OOMModel:
        def generate_content(self, prompt):
            raise Exception('Out of memory')

    monkeypatch.setattr(gemini_brain, 'genai', SimpleNamespace(GenerativeModel=lambda name: OOMModel(), configure=lambda api_key: None))

    res = gemini_brain.get_viral_script('topic')
    assert res == 'System Error. The AI refused to speak.'
