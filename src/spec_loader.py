from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EndpointSchema:
    path: str
    method: str
    response_schema: dict[str, Any]
    required_fields: list[str]
    base_url: str


def _resolve_spec_path(paths: dict[str, Any], endpoint: str) -> str:
    path_only = endpoint.split("?", 1)[0]
    candidates = [endpoint, path_only]
    if path_only.endswith("/"):
        candidates.append(path_only.rstrip("/"))
    else:
        candidates.append(f"{path_only}/")

    for candidate in candidates:
        if candidate in paths:
            return candidate

    raise ValueError(f"Endpoint '{endpoint}' not found in spec.")


def load_endpoint_schema(spec_path: Path, endpoint: str, method: str = "get") -> EndpointSchema:
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    method = method.lower()

    paths = data.get("paths", {})
    spec_path_key = _resolve_spec_path(paths, endpoint)
    endpoint_data = paths[spec_path_key].get(method)
    if not endpoint_data:
        raise ValueError(f"Method '{method}' not found for endpoint '{endpoint}'.")

    response_200 = endpoint_data.get("responses", {}).get("200") or endpoint_data.get("responses", {}).get("201")
    if not response_200:
        raise ValueError("No 200/201 response schema found for endpoint.")

    content = response_200.get("content", {}).get("application/json", {})
    schema = content.get("schema")
    if not schema:
        raise ValueError("No application/json schema found for response.")

    required = schema.get("required", [])
    response_schema = schema
    if schema.get("type") == "array":
        items = schema.get("items", {})
        response_schema = items
        required = items.get("required", [])

    servers = data.get("servers", [])
    base_url = servers[0]["url"] if servers else ""

    return EndpointSchema(
        path=endpoint,
        method=method,
        response_schema=response_schema,
        required_fields=required,
        base_url=base_url,
    )
