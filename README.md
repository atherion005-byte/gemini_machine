# GEMINI_MACHINE

Small demo pipeline that builds short vertical videos from a trending topic.

## Configuration

- Set the Gemini API key via environment variable:

  - Windows (PowerShell):

    ```powershell
    $env:GOOGLE_API_KEY = "your-api-key"
    ```

  - Linux / macOS (bash):

    ```bash
    export GOOGLE_API_KEY="your-api-key"
    ```

- You can run a quick local test of the Gemini integration:

  ```bash
  python gemini_brain.py "Your Topic"
  ```

- Use the provided `.env.example` as a template. Copy it to `.env` and fill in your real keys (do NOT commit real secrets):

  ```bash
  cp .env.example .env
  # then edit .env to add your keys
  ```

## Tests

- Install dev dependencies and run tests:

  ```bash
  pip install pytest
  pytest -q
  ```

## CI

A GitHub Actions workflow is included to run tests on push and pull requests.
