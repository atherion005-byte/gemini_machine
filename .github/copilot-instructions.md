# Copilot / AI Agent Instructions

Goal: Get productive quickly with the GEMINI_MACHINE repo. This file contains concrete, repository-specific patterns, commands, and constraints an AI agent should follow.

## Big picture
- This repo builds vertical short videos from a trending topic: fetch trend -> generate script -> synthesize audio -> create visuals -> compose final MP4.
- Key orchestrator: `run_machine.py` (trending → `gemini_brain.get_viral_script` → `free_voice.generate_audio` → `free_vision.generate_video_file`).
- Alternative pipelines exist (local-only and VEO/video API paths): see `gatling_final.py`, `glitch_core.py`, `veo_brain.py`, `imagen_brain.py`, and `pexels_brain.py`.

## Important files & roles (examples)
- `run_machine.py` — main demo pipeline that uses Google Trends, Gemini text, gTTS, and MoviePy.
- `gemini_brain.py` — text generation via Google `generativeai`; contains retry logic for 429s and returns plain spoken text.
- `free_voice.py` — uses `gtts.gTTS` to write `temp_audio_{index}.mp3` files.
- `free_vision.py` — composes text on a black 9:16 background with MoviePy; explicit `IMAGEMAGICK_BINARY` path is set (Windows path in repo).
- `glitch_core.py` — local glitch/noise video generation (used by `gatling_final.py`).
- `veo_brain.py` / `imagen_brain.py` — wrappers for Google Video/Image model APIs (use client.operations polling/looping patterns).
- `pexels_brain.py` — downloads stock videos from Pexels API; uses `STOCK_BG_{index}.mp4` naming.

## Environment & developer workflows (explicit)
- To run the usual end-to-end demo: `python run_machine.py`.
- To run the local glitch-only pipeline: `python gatling_final.py`.
- Diagnostic: `python scan_weapons.py` lists available Google models in your account and warns if VEO/video models are missing.

Install (observed) Python dependencies (examples):
- moviepy, pillow (PIL), numpy, gtts, pytrends, requests, google-generativeai (or `google` with `genai` submodule)
- ImageMagick is required for MoviePy text rendering; the repo hard-codes a Windows path:
  - `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe`
  - If your system differs, update the `change_settings({'IMAGEMAGICK_BINARY': ...})` lines in `free_vision.py`, `glitch_core.py`, and `gatling_final.py`.

## Project-specific conventions & patterns
- Files expose a small set of side-effecting functions that write files to the repo working dir (e.g., `temp_audio_0.mp3`, `GLITCH_BG_0.mp4`, `FINAL_UPLOAD_0_<TOPIC>.mp4`).
- Print-based progress logging is used extensively; preserve human-readable `print()` output when editing flows.
- API usage patterns:
  - `gemini_brain.get_viral_script()` shows a retry-on-429 pattern — follow it when calling Generative models.
  - `imagen_brain.generate_visual_asset()` tries multiple `TARGET_MODELS` in order; keep that ordered-fallback behavior.
  - `veo_brain.generate_veo_asset()` polls an operation until `operation.done` — do not replace with fire-and-forget.
- Naming: use existing filename conventions when creating assets (e.g., `VEO_UPLOAD_{i}_{topic}.mp4`, `VISUAL_BG_{i}.png`).

## Secrets & safety rules (must follow)
- Many modules currently hardcode API keys (e.g., `gemini_brain.py`, `veo_brain.py`, `pexels_brain.py`, `scan_weapons.py`).
  - Never commit new keys.
  - When changing code, prefer `os.environ.get('GOOGLE_API_KEY')` / `PEXELS_API_KEY` and document the expected env var names.
- Treat any API key or secret in the repo as PII/secret and avoid exposing it in PRs or logs.

## Known quirks and actionable constraints
- IMAGEMAGICK_BINARY is hard-coded to a Windows path in multiple files; on other platforms this must be changed.
- `veo_brain.py` notes: do NOT pass `generate_audio=True` in the request (it caused a crash for this codebase). Respect in-file comments when using model APIs.
- The repo uses both `google.generativeai as genai` and `from google import genai` patterns — be conservative when refactoring imports.
- `free_vision.py` expects fonts like `Arial-Bold` and `Courier` for TextClip; tests may fail if fonts are missing—either bundle availability checks or pick fallback fonts.

## Safety for code changes (guidelines for patches)
- Prefer small, well-scoped changes with manual verification (run `python run_machine.py` or `python gatling_final.py` locally and confirm a file is produced).
- When modifying API interaction: preserve retry and fallback behavior (429 handling, model fallbacks, operation polling).
- When introducing configuration (e.g., env var names, new settings), add a short top-level comment to the edited file explaining the config key expected.

## Quick examples (copyable snippets)
- Use env var for API key (example):
  - `API_KEY = os.environ.get('GOOGLE_API_KEY') or '<fallback>'`
- Polling pattern (VEO):
  - keep the `while not operation.done: time.sleep(10); operation = client.operations.get(operation)` loop
- Fallback model loop (Imagen):
  - try models from `TARGET_MODELS` sequentially and continue to the next on exceptions.

---
If anything here is unclear or you'd like more details (e.g., a suggested `requirements.txt` or help moving keys into env vars and creating a `.env.example`), tell me which part to expand and I will update this file. ✅
