# Repository Guidelines

## Project Structure & Module Organization
- `test_case/`: pytest suites. Current tests include `test_case/login/test_login.py` and request utility checks.
- `util/`: reusable helpers.
- `util/requestsUtils/requestControl.py`: HTTP request wrapper.
- `util/readFileUtils/`: YAML readers and test-case parsing.
- `data/`: test data YAML files (for example `data/login.yaml`).
- `common/`: runtime configuration (`common/config.yaml`, env resolution in `common/config.py`).
- `run.py`: local smoke entry for YAML case parsing.
- `docs/`: project notes and setup documentation.

## Build, Test, and Development Commands
- `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`: create and activate local virtualenv.
- `pip install -r requirements.txt`: install pytest, requests, PyYAML, allure adapter, and helpers.
- `pytest`: run all tests (`pytest.ini` already sets `testpaths = test_case`, `-q -s`).
- `pytest test_case/login/test_login.py -q -s`: run one module while iterating.
- `python run.py`: print parsed case list from `data/login.yaml` for quick validation.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and readable line lengths.
- Use `snake_case` for functions, variables, and modules; use `PascalCase` for classes (for example `RequestControl`).
- Name tests `test_*.py`, and test functions `test_*` so pytest can discover them.
- Keep YAML data keys stable (`url`, `method`, `headers`, `data`, `assert`) to match parser logic.

## Collaboration Workflow
- When the user explicitly asks to review or explain a refactor idea first, do not modify business code immediately.
- In that situation, first provide a concrete code-shaped proposal with a small amount of explanation, wait for confirmation, and only then edit the project code.
- Instruction or documentation updates requested by the user (for example `AGENTS.md`) may still be applied first if they do not change runtime behavior.

## Testing Guidelines
- Framework: `pytest` with `@pytest.mark.parametrize` for YAML-driven cases; `allure-pytest` for reporting metadata.
- Add at least one positive assertion per case (`status_code` minimum), then extend with body/content checks when needed.
- No enforced coverage gate exists yet; target meaningful coverage for request flow and YAML parsing before merge.

## Commit & Pull Request Guidelines
- Existing history uses short Chinese summaries. Keep commits concise, imperative, and scoped (example: `login: add status code assertion`).
- One logical change per commit; avoid mixing refactor and behavior changes.
- PRs should include change purpose and affected paths, exact verification command, and sample output or screenshots when behavior changes.

## Security & Configuration Tips
- Do not commit secrets/tokens in `common/config.yaml` or test data files.
- Keep environment host values configurable via `common/config.yaml` instead of hard-coding URLs in test code.
