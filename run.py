from __future__ import annotations

import argparse
import json
from pathlib import Path

import httpx
from dotenv import load_dotenv

from src.llm_oracle_miner import mine_constraints_with_oc
from src.spec_loader import load_endpoint_schema
from src.validator import validate_constraints


def main() -> None:
    load_dotenv()
    args = parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    endpoint_schema = load_endpoint_schema(Path(args.spec), args.endpoint, args.method)

    base_url = args.base_url or endpoint_schema.base_url
    if not base_url:
        raise ValueError("Base URL missing. Provide --base-url or set servers[0].url in spec.")

    constraints, source = mine_constraints_with_oc(
        schema=endpoint_schema.response_schema,
        required_fields=endpoint_schema.required_fields,
        model=args.model,
    )
    constraints_path = out_dir / "mined_constraints.json"
    constraints_path.write_text(json.dumps(constraints, indent=2), encoding="utf-8")

    response_json = fetch_response(
        base_url=base_url,
        endpoint=args.endpoint,
        method=args.method,
        path_param=args.path_param,
        timeout=args.timeout,
    )
    response_path = out_dir / "response.json"
    response_path.write_text(json.dumps(response_json, indent=2), encoding="utf-8")

    results = validate_constraints(response_json, constraints)
    results_path = out_dir / "validation_results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    pass_count = len(results) - fail_count

    print("=== RBCTest-style Oracle Mining Demo ===")
    print(f"Source: {source}")
    print(f"Spec: {args.spec}")
    print(f"Endpoint: {args.method.upper()} {args.endpoint}")
    print(f"Response saved: {response_path}")
    print(f"Constraints saved: {constraints_path}")
    print(f"Results saved: {results_path}")
    print(f"Summary: PASS={pass_count}, FAIL={fail_count}")
    print("\nTop checks:")
    for row in results[:10]:
        print(f"- [{row['status']}] {row['id']} :: {row['detail']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Small RBCTest-style oracle miner.")
    parser.add_argument("--spec", default="spec/sample-openapi.yaml", help="Path to OpenAPI spec.")
    parser.add_argument("--endpoint", default="/users/{id}", help="Endpoint path in spec.")
    parser.add_argument("--method", default="get", choices=["get", "post", "put", "patch", "delete"])
    parser.add_argument("--base-url", default="", help="Override base URL.")
    parser.add_argument("--path-param", default="id=1", help="Single path param in key=value form.")
    parser.add_argument("--model", default="claude-3-5-sonnet-latest", help="Anthropic model name.")
    parser.add_argument("--output-dir", default="output", help="Directory for generated artifacts.")
    parser.add_argument("--timeout", type=float, default=20.0)
    return parser.parse_args()


def fetch_response(
    base_url: str, endpoint: str, method: str, path_param: str, timeout: float
) -> dict:
    key, val = path_param.split("=", maxsplit=1)
    rendered = endpoint.replace(f"{{{key}}}", val)
    url = f"{base_url.rstrip('/')}{rendered}"

    with httpx.Client(timeout=timeout) as client:
        resp = client.request(method.upper(), url)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise ValueError("This starter expects an object JSON response.")
        return data


if __name__ == "__main__":
    main()
