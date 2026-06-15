# RBCTest-Style Oracle Mining Starter

Tiny, runnable starter that mirrors the core RBCTest loop:

1. Read one OpenAPI response schema
2. Mine response-body constraints (oracles) with an LLM
3. Confirm constraints in a second pass (Observation-Confirmation style)
4. Fetch a real API response
5. Validate PASS/FAIL and save artifacts

This is a small learning/demo scaffold inspired by:
- Paper: https://arxiv.org/abs/2504.17287
- Repo: https://github.com/api-rbtest/RBCTest

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add ANTHROPIC_API_KEY in .env (optional but recommended)
python run.py
```

Output files are written to `output/`:
- `output/mined_constraints.json`
- `output/response.json`
- `output/validation_results.json`

## Defaults

The included sample spec targets:
- `GET /users/{id}`
- Base URL: `https://jsonplaceholder.typicode.com`

Run with defaults:

```bash
python run.py
```

Use your own endpoint/spec:

```bash
python run.py \
  --spec spec/your-openapi.yaml \
  --endpoint /products/{id} \
  --method get \
  --base-url https://your-api.example.com \
  --path-param id=123
```

## Notes

- If `ANTHROPIC_API_KEY` is missing, the tool uses a deterministic fallback miner (type/required/enum/email rules) so you can still run the flow end-to-end.
- Keep API keys, private URLs, and proprietary payloads out of the repo.
