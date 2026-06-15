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


def load_endpoint_schema(spec_path: Path, endpoint: str, method: str = "get") -> EndpointSchema:
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    method = method.lower()

    paths = data.get("paths", {})
    if endpoint not in paths:
        raise ValueError(f"Endpoint '{endpoint}' not found in spec.")

    endpoint_data = paths[endpoint].get(method)
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
    servers = data.get("servers", [])
    base_url = servers[0]["url"] if servers else ""

    return EndpointSchema(
        path=endpoint,
        method=method,
        response_schema=schema,
        required_fields=required,
        base_url=base_url,
    )
