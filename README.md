# RBCTest-Style Oracle Mining Starter

Tiny, runnable starter that mirrors the core RBCTest loop:

1. Read one OpenAPI response schema
2. Mine response-body constraints (oracles) with an LLM
3. Confirm constraints in a second pass (Observation-Confirmation style)
4. Load a sanitized fixture response (or fetch live with `--live`)
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
# add GROQ_API_KEY and API_BASE_URL in .env (optional but recommended)
python run.py
```

Output files are written to `output/`:
- `output/mined_constraints.json`
- `output/response.json`
- `output/validation_results.json`

## Defaults

The included sample spec targets:
- `GET /shop/2/category/4/items/?start=0&limit=10&language_code=en`
- Response fixture: `fixtures/shop_items_response.json` 

Run with defaults:

```bash
cd rbctest-starter
source .venv/bin/activate
python run.py
```

Fetch from the live API instead:

```bash
python run.py --live
```

See `output/report.md` for the full PASS/FAIL breakdown (mismatches are deduplicated per field).

### Schema mismatches: null on non-nullable fields

When the API returns `null` for a field that is **not** marked `nullable: true` in the spec, schema validation fails with:

`null returned but field is not nullable in spec`

The demo fixture sets `null` on required non-nullable fields such as `name`, `code`, and `sell_price` while leaving nullable fields (`name_en`, `image`, etc.) as either values or allowed `null`.

### Nullable fields and downstream assumptions

The demo spec marks several item fields as `nullable: true` (`name_en`, `image`, `discount_price`, `discounted_quantity`). Schema validation **allows** `null` for those fields.

A second oracle layer checks **downstream assumptions**: consumers that treat nullable fields as always present. When the fixture returns `null`, schema checks pass but downstream checks fail with:

`nullable in spec but downstream assumes present (value=None)`

Use your own endpoint/spec:

```bash
python run.py \
  --spec spec/your-openapi.yaml \
  --endpoint /shop/2/category/4/items/ \
  --method get \
  --path-param ""
```

Query parameters can be appended to `--endpoint` (e.g. `?start=0&limit=10&language_code=en`). Override the base URL with `API_BASE_URL` in `.env` or `--base-url`.

## Notes

- If `GROQ_API_KEY` is missing, the tool uses a deterministic fallback miner (type/required/enum/email rules) so you can still run the flow end-to-end.
- Keep API keys, private URLs, and proprietary payloads out of the repo.
