# Repository Guidelines

## Project Overview

- This repository is a lightweight API automation framework built around `pytest + requests + yaml + allure`.
- The main business scenario is the order main flow in `test_case/test_order_main_flow.py`, which calls module YAML cases step by step and keeps business decisions in Python.
- The core runtime chain is: YAML case -> placeholder resolution -> HTTP request -> assertion -> extraction -> context storage.

## Project Structure & Ownership

- `test_case/test_order_main_flow.py`: ordered main-flow tests that reuse shared context through the `flow_context` fixture.
- `test_case/test_framework_basics.py`: local framework-level checks for request sending, placeholder resolution, assertions, and extraction.
- `test_case/login/test_login.py`: login YAML example test module. It currently keeps a manual request/assert style and its method is not named `test_*`, so pytest does not collect it in the current state.
- `test_case/test_request.py`: request smoke example. Its function is currently not named `test_*`, so pytest does not collect it unless the function is renamed.
- `util/case_runner.py`: the preferred entry point for running a single YAML case by `yaml_name + case_id`.
- `util/requestsUtils/requestControl.py`: request wrapper, host assembly, default headers, bearer token injection, and request debug info.
- `util/assertion/assert_control.py`: unified assertion engine for `status_code` and JSONPath-based business assertions.
- `util/extract/extract_control.py`: response extraction engine for plain JSONPath extraction.
- `util/context/context_manager.py`: in-memory shared context used across a flow for values such as `token`, `product_id`, `unique`, and `cartId`.
- `util/readFileUtils/`: YAML reading, case parsing, and placeholder replacement.
- `common/config.yaml`: environment configuration and current default environment.
- `common/config.py`: exposes `HOST` from the selected environment.
- `conftest.py`: pytest fixtures for context cleanup plus an unfinished environment-switching implementation. `flow_context`, `case_context`, and `login_init` are present; the `--env` switching path currently needs code fixes before it can be relied on.
- `report/`: generated allure result and HTML report output. Treat as generated artifacts, not source code.
- `_external_pytest_auto_api2/`: external reference material. Do not modify it unless the user explicitly asks.

## Build, Test, and Development Commands

- `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`: create and activate a local virtual environment.
- `pip install -r requirements.txt`: install project dependencies.
- `pytest`: run all collected tests. `pytest.ini` already sets `testpaths = test_case` and writes allure results to `report/tmp`.
- `pytest --collect-only -q`: verify whether test files and methods are actually discoverable. In the current repo state, this collects `test_framework_basics.py` and `test_order_main_flow.py`, but not `test_case/login/test_login.py` or `test_case/test_request.py`.
- `pytest test_case/test_order_main_flow.py -q -s`: run the order main flow only.
- `pytest test_case/test_framework_basics.py -q -s`: run local framework checks only.
- `pytest --env=test` or `pytest --env=prod`: intended way to switch target environment through the fixture layer, but the current `conftest.py` implementation is incomplete and will error until fixed.
- `python run.py`: invoke pytest from Python and then generate the allure HTML report into `report/html`.
- `python run.py test_case/test_order_main_flow.py`: run a specific test target through `run.py`.
- `run.py` depends on a locally available `allure` CLI for HTML report generation.

## YAML Case Conventions

- Put executable API case data in `data/*.yaml`.
- Keep executable case keys aligned with the current runtime contract: `url`, `method`, `headers`, `params`, `data`, `assert`, and `extract`.
- Put shared fields in `case_common` so the YAML parser can merge them into each case.
- Use `${{variable_name}}` for placeholders. Resolve values through `ContextManager`.
- Do not invent new function-style placeholders casually. Keep `${{host()}}` semantics aligned with `util/readFileUtils/placeholder.py`.
- Use relative URLs such as `/login` and let `RequestControl` combine them with `HOST`.
- Add plain JSONPath `extract` rules for direct response values needed by later steps. Keep business selections such as choosing an in-stock `unique` in the Python flow test.

## Assertion & Extraction Rules

- Give every API case at least one positive assertion. `status_code` is the minimum requirement.
- Write JSON body assertions with the current structure: `jsonpath`, `type`, and `value`.
- Only use assertion operators supported by `AssertControl`: `eq`, `==`, `equals`, `ne`, `!=`, `in`, `contains`, and `exists`.
- Only use extraction rules supported by `ExtractControl`: plain JSONPath expressions.
- If you extend assertion or extraction syntax, update the corresponding utility code and add coverage in `test_case/test_framework_basics.py`.

## Coding Style & Naming Conventions

- Follow PEP 8 with 4-space indentation and readable line lengths.
- Use `snake_case` for functions, variables, and modules.
- Use `PascalCase` for classes such as `RequestControl`, `AssertControl`, `ExtractControl`, and `ContextManager`.
- Name pytest files `test_*.py` and test functions or methods `test_*` so pytest collects them reliably.
- Use `run_case()` as the preferred entry point for new YAML-driven API execution instead of duplicating request/assert/extract logic in each test.
- For new YAML-driven business cases, use the pattern `prepare YAML -> call run_case(yaml_name, case_id)` in tests. The current `test_case/login/test_login.py` is still a manual example and can be treated as legacy style rather than the target pattern.
- Do not hard-code hosts or tokens in test code.

## Collaboration Workflow

- If the user explicitly asks to review or explain a refactor idea first, do not modify business code immediately.
- In that situation, first provide a concrete code-shaped proposal with a small amount of explanation, wait for confirmation, and only then edit runtime code.
- You may apply documentation or instruction updates requested by the user, including `AGENTS.md`, before runtime code changes because they do not change runtime behavior.
- If you touch request, parser, assertion, extraction, or context behavior, verify the related tests and mention any environment-dependent limits in your handoff.
- Treat generated files under `report/`, `.pytest_cache/`, and `__pycache__/` as artifacts, not as the source of truth.

## Testing Guidelines

- Cover framework-level behavior in `test_case/test_framework_basics.py` whenever possible.
- Cover single-interface request data and assertions in module YAML, and keep flow order and business decisions in `test_case/test_order_main_flow.py`.
- Preserve context isolation by reusing existing fixtures such as `flow_context` and `case_context` when adding new tests.
- For order main flow changes, protect the extraction chain across steps instead of validating each request in isolation only.
- Before relying on a test module, confirm that pytest collects it. A file under `test_case/` is not enough if its function or method names do not start with `test_`. In the current repo state, `test_case/login/test_login.py` and `test_case/test_request.py` are examples of files that exist under `test_case/` but are not collected.

## Commit & Pull Request Guidelines

- Existing history favors short Chinese summaries. Keep commits concise, imperative, and scoped.
- One logical change per commit. Do not mix framework refactors, YAML changes, and unrelated documentation changes unless the user asks for that grouping.
- PRs should include change purpose, affected paths, exact verification commands, and representative output when behavior changes.

## Security & Configuration Tips

- Do not commit secrets, tokens, or private credentials into `common/config.yaml`, YAML test data, or report artifacts.
- Keep environment-specific hosts configurable through `common/config.yaml` and fixture-driven switching, not hard-coded in business tests.
- Be cautious with real external hosts in flow tests. Prefer configuration changes over code edits when switching environments.

# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
