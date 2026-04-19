# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt

# Run all tests (with Allure results generated in ./report/tmp)
pytest

# Run tests with a specific environment (test/prod)
pytest --env prod

# Run a single test module
pytest test_case/login/test_login.py -q -s

# Run a single test by name/keyword
pytest test_case/test_order_main_flow.py -q -s -k test_product_list

# Run tests and generate Allure HTML report (via run.py)
python run.py

# Run tests on a specific file (via run.py)
python run.py test_case/login/test_login.py
```

`pytest.ini` sets `testpaths = test_case`, `addopts = -q -s --alluredir=./report/tmp --clean-alluredir`, and `pythonpath = .`, so running bare `pytest` discovers everything under `test_case/` and stores Allure results. Use `run.py` to generate the HTML report (or run `allure generate ./report/tmp -o ./report/html --clean` manually).

## Architecture

This is a **YAML-driven API test automation framework**. The core flow is:

```
data/*.yaml  →  readFileUtils  →  RequestControl  →  AssertControl / ExtractControl
```

### Data Layer (`data/`)
YAML files define test cases. Each file has an optional `case_common` block (merged into every case) and named case blocks whose keys act as `case_id`s. Example schema:

```yaml
case_common:
  allureEpic: ...

login:                          # case_id
  host: ${{host()}}             # placeholder resolved at load time
  url: /login
  method: post
  headers: { Content-Type: application/json;charset=UTF-8 }
  data: { account: ..., password: ... }
  assert:
    status_code: 200
    msg:
      jsonpath: $.msg
      type: in          # supported: eq, ne, in, contains, exists
      value: 登录成功
```

The `${{host()}}` placeholder is resolved by `util/readFileUtils/placeholder.py` to the `HOST` value from `common/config.yaml`.

### Configuration (`common/`)
- `config.yaml` — multi-environment host URLs; `current_env` selects active env (`test` or `prod`).
- `config.py` — reads `HOST` from the active environment; imported by `placeholder.py`.
- `setting.py` — `root_path()` and `ensure_path_sep()` for cross-platform path resolution.

Environment can be switched at runtime via the `--env` command‑line flag (see **Commands**). The `conftest.py` fixture `active_env` patches the `HOST` variable in all relevant modules.

### Utility Layer (`util/`)
| Module | Class | Purpose |
|---|---|---|
| `readFileUtils/yamlControl.py` | `yamlControl` | Low-level YAML file reader (handles relative → absolute paths) |
| `readFileUtils/get_yaml_data_analysis.py` | — | `get_case_list(yaml)` → `[(case_id, case_dict), ...]`; `get_case_by_id(yaml, id)` for single lookup |
| `readFileUtils/placeholder.py` | — | Resolves `${{host()}}` in loaded YAML data |
| `requestsUtils/requestControl.py` | `RequestControl` | Session-based HTTP wrapper; returns `{status_code, body, text, headers, request_debug}` |
| `assertion/assert_control.py` | `AssertControl` | Validates `assert` block: status code first, then JSONPath rules per field |
| `extract/extract_control.py` | `ExtractControl` | Runs JSONPath exprs from `extract` block and stores results in `ContextManager` |
| `context/context_manager.py` | `ContextManager` | Class-level dict for sharing extracted values across steps in a flow |
| `case_runner.py` | — | `run_case(yaml_name, case_id, client=None)` – convenient wrapper that loads a case, sends request, runs assertion and extraction |

### Test Layer (`test_case/`)
- **Parametrized tests** (`test_login.py`): use `@pytest.mark.parametrize("case_id, case", get_case_list("login.yaml"))` — one test invocation per YAML case.
- **Sequential flow tests** (`test_order_main_flow.py`): call `get_case_by_id()` per test method to run a named step; use `ContextManager` to pass extracted values between steps.

### Fixtures (`conftest.py`)
- `active_env` – reads `--env` flag and patches `HOST` in `common.config`, `util.requestsUtils.requestControl`, and `util.readFileUtils.placeholder`. Yields `{"name": env_name, "host": host}`.
- `apply_env` – automatically applies the environment switch (autouse session fixture).
- `flow_context` – class‑level fixture that clears `ContextManager` before and after a test class.
- `case_context` – function‑level fixture that clears `ContextManager` before and after a single test.
- `login_init` – example fixture that runs the `login` case from `order_main_flow.yaml` and returns its response.

### Adding a New Test
1. Add case(s) to an existing `data/*.yaml` or create a new YAML file.
2. Either add a parametrize‑based test class (for independent cases) or individual test methods calling `get_case_by_id()` (for ordered flows).
3. Use `AssertControl(...).run()` for assertions; `ExtractControl(...).run()` if values must be forwarded to later steps.
4. For concise step execution, consider using `run_case()` from `util.case_runner`.
5. Use the `flow_context` or `case_context` fixtures to ensure clean context for each test class or function.

### Allure Reporting
Allure results are automatically written to `./report/tmp` by pytest (configured in `pytest.ini`). Generate the HTML report with `run.py` or manually via `allure generate ./report/tmp -o ./report/html --clean`. The report includes test metadata and steps.

### Collaboration Guidelines
See `AGENTS.md` for detailed coding style, collaboration workflow, commit conventions, and security tips.