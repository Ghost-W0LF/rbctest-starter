from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

from src.llm_oracle_miner import mine_constraints_with_oc
from src.schema_constraints import (
    dedupe_failures_by_field,
    expand_array_constraints,
    extract_downstream_constraints,
    extract_schema_constraints,
    merge_constraints,
)
from src.spec_loader import load_endpoint_schema
from src.validator import validate_constraints


def main() -> None:
    load_dotenv()
    args = parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    endpoint_schema = load_endpoint_schema(Path(args.spec), args.endpoint, args.method)

    base_url = resolve_base_url(args, endpoint_schema)
    if not base_url:
        raise ValueError(
            "Base URL missing. Set API_BASE_URL in .env, pass --base-url, or set servers[0].url in spec."
        )

    llm_constraints, source = mine_constraints_with_oc(
        schema=endpoint_schema.response_schema,
        required_fields=endpoint_schema.required_fields,
        model=args.model,
    )
    schema_constraints = extract_schema_constraints(endpoint_schema.response_schema)
    downstream_constraints = extract_downstream_constraints(endpoint_schema.response_schema)
    constraints = merge_constraints(llm_constraints, schema_constraints, downstream_constraints)

    response_json = load_response(args, base_url)
    response_path = out_dir / "response.json"
    response_path.write_text(json.dumps(response_json, indent=2), encoding="utf-8")

    constraints = expand_array_constraints(constraints, response_json)
    constraints_path = out_dir / "mined_constraints.json"
    constraints_path.write_text(json.dumps(constraints, indent=2), encoding="utf-8")

    results = validate_constraints(response_json, constraints)
    results_path = out_dir / "validation_results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    report_path = out_dir / "report.md"
    report_path.write_text(build_report(args, source, constraints, results), encoding="utf-8")

    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    pass_count = len(results) - fail_count
    schema_failures, downstream_failures = split_failures(results)
    failures = schema_failures + downstream_failures

    print("=== RBCTest-style Oracle Mining Demo ===")
    print(f"Source: {source}")
    print(f"Spec: {args.spec}")
    print(f"Endpoint: {args.method.upper()} {args.endpoint}")
    if args.response:
        print(f"Response fixture: {args.response}")
    else:
        print(f"Response: live API ({base_url})")
    print(f"Response saved: {response_path}")
    print(f"Constraints saved: {constraints_path}")
    print(f"Results saved: {results_path}")
    print(f"Report saved: {report_path}")
    print(f"Summary: PASS={pass_count}, FAIL={fail_count} (unique mismatch fields: {len(failures)})")
    ordered_results = failures + [r for r in results if r["status"] == "PASS"]
    print("\nAll checks:")
    for row in ordered_results:
        print(f"- [{row['status']}] {row['field']} :: {row['detail']}")

    if schema_failures:
        print("\nSchema mismatches:")
        for row in schema_failures:
            print(f"- {row['field']}: {row['detail']}")

    if downstream_failures:
        print("\nDownstream assumption mismatches (nullable field assumed present):")
        for row in downstream_failures:
            print(f"- {row['field']}: {row['detail']}")

    if not failures:
        print("\nNo mismatches found. Tighten the spec or try another endpoint.")


def split_failures(results: list[dict]) -> tuple[list[dict], list[dict]]:
    all_failures = [r for r in results if r["status"] == "FAIL"]
    downstream = dedupe_failures_by_field(
        [r for r in all_failures if r.get("constraint_type") == "downstream_present"]
    )
    schema = dedupe_failures_by_field(
        [r for r in all_failures if r.get("constraint_type") != "downstream_present"]
    )
    return schema, downstream


def build_report(
    args: argparse.Namespace,
    source: str,
    constraints: list[dict],
    results: list[dict],
) -> str:
    schema_failures, downstream_failures = split_failures(results)
    failures = schema_failures + downstream_failures
    passes = [r for r in results if r["status"] == "PASS"]

    lines = [
        "# Oracle Mining Report",
        "",
        f"- Endpoint: `{args.method.upper()} {args.endpoint}`",
        f"- Mining source: `{source}`",
        f"- Constraints checked: {len(constraints)}",
        f"- PASS: {len(passes)}",
        f"- FAIL: {sum(1 for r in results if r['status'] == 'FAIL')}",
        f"- Unique mismatch fields: {len(failures)}",
        "",
    ]

    if schema_failures:
        lines.extend(["## Schema mismatches (spec vs reality)", ""])
        for i, row in enumerate(schema_failures, start=1):
            lines.extend(
                [
                    f"### Schema mismatch #{i}",
                    f"- Field: `{row['field']}`",
                    f"- Rule: {row['rule']}",
                    f"- Detail: {row['detail']}",
                    "",
                ]
            )

    if downstream_failures:
        lines.extend(
            [
                "## Downstream assumption mismatches (nullable field assumed present)",
                "",
            ]
        )
        for i, row in enumerate(downstream_failures, start=1):
            lines.extend(
                [
                    f"### Downstream mismatch #{i}",
                    f"- Field: `{row['field']}`",
                    f"- Rule: {row['rule']}",
                    f"- Detail: {row['detail']}",
                    "",
                ]
            )

    if not failures:
        lines.append("No mismatches detected.")

    lines.extend(["## All checks", ""])
    ordered_results = failures + passes
    for row in ordered_results:
        lines.append(f"- [{row['status']}] `{row['field']}` :: {row['detail']}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Small RBCTest-style oracle miner.")
    parser.add_argument("--spec", default="spec/sample-openapi.yaml", help="Path to OpenAPI spec.")
    parser.add_argument(
        "--endpoint",
        default="/shop/2/category/4/items/?start=0&limit=10&language_code=en",
        help="Endpoint path in spec (query string may be included).",
    )
    parser.add_argument("--method", default="get", choices=["get", "post", "put", "patch", "delete"])
    parser.add_argument("--base-url", default="", help="Override base URL (defaults to API_BASE_URL in .env).")
    parser.add_argument("--path-param", default="", help="Single path param in key=value form.")
    parser.add_argument("--model", default="llama-3.3-70b-versatile", help="Groq model name.")
    parser.add_argument("--output-dir", default="output", help="Directory for generated artifacts.")
    parser.add_argument(
        "--response",
        default="fixtures/shop_items_response.json",
        help="Path to sanitized/synthetic response JSON. Use --live to fetch from the API instead.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch response from the live API instead of a fixture file.",
    )
    parser.add_argument("--timeout", type=float, default=20.0)
    return parser.parse_args()


def resolve_base_url(args: argparse.Namespace, endpoint_schema) -> str:
    return (args.base_url or os.getenv("API_BASE_URL", "") or endpoint_schema.base_url).strip()


def load_response(args: argparse.Namespace, base_url: str) -> dict:
    if args.live:
        return fetch_response(
            base_url=base_url,
            endpoint=args.endpoint,
            method=args.method,
            path_param=args.path_param,
            timeout=args.timeout,
        )

    response_path = Path(args.response)
    if not response_path.is_file():
        raise ValueError(f"Response fixture not found: {response_path}")

    data = json.loads(response_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        if not data:
            raise ValueError("Empty list response.")
        data = data[0]
    if not isinstance(data, dict):
        raise ValueError("This starter expects an object JSON response.")
    return data


def fetch_response(
    base_url: str, endpoint: str, method: str, path_param: str, timeout: float
) -> dict:
    rendered = endpoint
    if path_param:
        key, val = path_param.split("=", maxsplit=1)
        rendered = endpoint.replace(f"{{{key}}}", val)
    url = f"{base_url.rstrip('/')}{rendered}"

    with httpx.Client(timeout=timeout) as client:
        resp = client.request(method.upper(), url)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            if not data:
                raise ValueError("Empty list response.")
            data = data[0]
        if not isinstance(data, dict):
            raise ValueError("This starter expects an object JSON response.")
        return data


if __name__ == "__main__":
    main()
