# BLOCK_PROTOCOL.md  
Standards every PrometheusBlocks utility must follow
====================================================

## 1. Purpose

This template lets any developer — human or AI — create a block that
“just works” with the PrometheusBlocks orchestrator.  
Follow the rules below and your block will lint, test, publish, and
auto-register without extra setup.

---

## 2. Required files & directories

| Path / Directory                 | Must contain                                           |
|----------------------------------|--------------------------------------------------------|
| `.github/workflows/ci.yml`       | CI pipeline (Black check, Flake8, pytest, token gate)  |
| `.flake8`                        | `extend-ignore = E401,E501`, `max-line-length = 120`   |
| `scripts/token_check.py`         | Enforces ≤ 200 000 tokens for all `.py` files          |
| `utility_contract.json`          | Block’s manifest — overwrite the stub                  |
| `models/`, `service/`, `tests/`  | Implementation code and unit tests (add at least one) |
| `_reference/utility_contract.py` | **Schema class** — read-only, do not modify           |

Files inside `_reference/` are ignored by Flake8 and the token checker.

---

## 3. Utility-contract schema (summary)

Every block must ship a **`utility_contract.json`** that validates
against the `UtilityContract` schema (see `_reference/utility_contract.py`).

```jsonc
{
  "name": "your-block",
  "version": "1.0.0",
  "language": "python",
  "description": "One-sentence purpose.",
  "size_budget": 200000,
  "entrypoints": [
    {
      "name": "do_something",
      "description": "What it does",
      "parameters_schema": {},
      "return_schema": {}
    }
  ],
  "deps": [
    { "package": "pydantic", "version": ">=2.6" }
  ],
  "tests": ["tests/test_core.py"]
}
4. Token-budget rule
scripts/token_check.py counts non-whitespace tokens in every .py file (excluding _reference, .venv).
CI fails if the total exceeds 200 000.

5. CI pass criteria

Tool	Passes when…
Black	black --check . returns 0
Flake8	No errors besides ignored rules
pytest	All tests green (or “No tests yet”)
6. Environment-switch convention
Blocks that expose pluggable back-ends use upper-case env vars, e.g.:

text
Copy
Edit
OCR_BACKEND = stub | tesseract | gpt4v
OPENAI_API_KEY = sk-…         # used only when OCR_BACKEND=gpt4v
Document additional vars in your block’s README.

7. Publishing a block
After CI is green and version set:

bash
Copy
Edit
pb-registry publish utility_contract.json
A copy named <name>-<version>.json appears in ~/.pb_registry/; the orchestrator catalog will list it.

8. Versioning rules
MAJOR — breaking change to the contract (rename/remove fields)

MINOR — backward-compatible additions

PATCH — fixes or internal refactors

9. Minimal block tree (example)
text
Copy
Edit
my-block/
├─ .github/workflows/ci.yml
├─ .flake8
├─ scripts/
│  └─ token_check.py
├─ models/
│  └─ account.py
├─ service/
│  └─ core.py
├─ tests/
│  └─ test_core.py
├─ utility_contract.json
├─ README.md
└─ _reference/
   └─ utility_contract.py
Follow this structure and your block will integrate automatically.