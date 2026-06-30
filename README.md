# RBCTest-Style Oracle Mining

A small, runnable tool that mines **test oracles** (response-body constraints) from an OpenAPI spec with an LLM, then checks them against real API responses to surface **spec-vs-reality mismatches**.

Inspired by RBCTest ([paper](https://arxiv.org/abs/2504.17287) · [repo](https://github.com/api-rbtest/RBCTest)).

## What this shows

- An LLM mines constraints from a response schema, then a **second confirmation pass** (Observation–Confirmation style) keeps only the constraints it can re-justify — reducing hallucinated oracles.
- Two oracle classes are checked: **schema constraints** (type / required / nullable) and **downstream assumptions** (fields a client treats as always-present that the spec actually marks nullable).
- On the bundled sample endpoint it checked **108 constraints → 98 PASS / 10 FAIL**, flagging **10 real mismatches** (e.g. non-nullable fields returning `null`, and nullable fields a client would crash on). See [`output/report.md`](output/report.md).
- Runs **with or without an LLM**: if no API key is set, a deterministic fallback miner (type/required/enum/email rules) still exercises the full pipeline.

## Pipeline

1. Load one OpenAPI response schema (`src/spec_loader.py`)
2. Mine response-body oracles with an LLM, observation–confirmation style (`src/llm_oracle_miner.py`)
3. Add schema + downstream constraints and merge (`src/schema_constraints.py`)
4. Load a sanitized fixture response (or fetch live with `--live`)
5. Validate PASS/FAIL and write artifacts (`src/validator.py`)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then add GROQ_API_KEY + API_BASE_URL (both optional)
python run.py
```

Artifacts are written to `output/`:

| File | Contents |
|---|---|
| `output/report.md` | Human-readable PASS/FAIL breakdown (**start here**) |
| `output/mined_constraints.json` | The oracles that were mined |
| `output/validation_results.json` | Per-field validation results |
| `output/response.json` | The response that was checked |

## Usage

Default run uses a sanitized fixture for `GET /shop/2/category/4/items/`:

```bash
python run.py
```

Fetch from the live API instead of the fixture:

```bash
python run.py --live
```

Point it at your own endpoint/spec:

```bash
python run.py \
  --spec spec/your-openapi.yaml \
  --endpoint "/your/endpoint/?limit=10" \
  --method get
```

Query parameters can be appended to `--endpoint`. Set the base URL via `API_BASE_URL` in `.env` or `--base-url`. Choose the model with `--model` (default `llama-3.3-70b-versatile`).

## Layout

```
run.py                     # CLI entrypoint + report builder
src/spec_loader.py         # parse OpenAPI response schema
src/llm_oracle_miner.py    # LLM mining + observation-confirmation pass
src/schema_constraints.py  # schema + downstream constraint extraction
src/validator.py           # PASS/FAIL checking
spec/sample-openapi.yaml   # sample spec
fixtures/                  # sanitized sample response
output/                    # generated artifacts
```

## Notes

- The bundled data is **synthetic/sanitized** — keep real API keys, private URLs, and proprietary payloads out of the repo.
- This is a compact demo/learning artifact, not a full reimplementation of RBCTest.
