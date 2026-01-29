# Repository Guidelines

## Project Structure & Module Organization
- `app/` contains the FastAPI backend and threat intelligence clients. Core integrations live in `app/core/`.
- `templates/` holds the HTML UI (`templates/dashboard.html`).
- `screenshots/` stores documentation images.
- `requirements.txt` defines Python dependencies.

## Build, Test, and Development Commands
- Move to the repo root: `cd /opt/zion`.
- Create and activate a virtual environment:
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`.
- Run the API locally (repo root): `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- Production service uses `uvicorn main:app` with `WorkingDirectory=/opt/zion/app` (see README’s systemd example).

## Configuration & Secrets
- Create a `.env` in the repo root with API tokens:
  - `SHODAN_API`, `VT_API`, `ABUSE_API`, `OTX_API`, `IPINFO_TOKEN`.
- Never commit real credentials. Use `.env` locally and keep it out of version control.

## Coding Style & Naming Conventions
- Python style mirrors existing code: 4-space indentation, `snake_case` for functions/vars, `CamelCase` for classes.
- Keep modules small and focused (each integration client per file in `app/core/`).
- There is no formatter or linter configured; keep changes consistent and readable.

## Testing Guidelines
- No automated tests are present today. If you add tests, create a `tests/` directory and keep filenames descriptive (e.g., `test_analyzer.py`).
- Prefer fast unit tests for API clients and parsing logic.

## Commit & Pull Request Guidelines
- Commit history favors short, imperative messages (e.g., “Update README.md”, “Add files via upload”).
- PRs should describe behavior changes, note new dependencies, and include screenshots when UI is affected.

## Security & Operational Notes
- This project is intended for authorized defensive use only; verify scope before scanning assets.
- Avoid committing sample data that could expose targets or credentials.
