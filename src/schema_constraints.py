from __future__ import annotations

from typing import Any


def extract_schema_constraints(schema: dict[str, Any], prefix: str = "") -> list[dict[str, Any]]:
    """Deterministically mine type/required/email constraints from an OpenAPI schema."""
    constraints: list[dict[str, Any]] = []
    props = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    for name, meta in props.items():
        path = f"{prefix}.{name}" if prefix else name

        if name in required_fields:
            constraints.append(
                {
                    "id": f"required_{path.replace('.', '_')}",
                    "field": path,
                    "kind": "response-property",
                    "rule": f"Field '{path}' must exist in response.",
                    "type": "required",
                    "confirmed": True,
                    "source": "schema",
                }
            )

        field_type = meta.get("type")
        if field_type == "object":
            constraints.extend(extract_schema_constraints(meta, path))
            continue

        if field_type in {"string", "integer", "number", "boolean", "array"}:
            constraints.append(
                {
                    "id": f"type_{path.replace('.', '_')}",
                    "field": path,
                    "kind": "response-property",
                    "rule": f"Field '{path}' must be of type '{field_type}'.",
                    "type": "type",
                    "expected_type": field_type,
                    "confirmed": True,
                    "source": "schema",
                }
            )

        if "enum" in meta:
            constraints.append(
                {
                    "id": f"enum_{path.replace('.', '_')}",
                    "field": path,
                    "kind": "response-property",
                    "rule": f"Field '{path}' must be one of allowed enum values.",
                    "type": "enum",
                    "allowed_values": meta["enum"],
                    "confirmed": True,
                    "source": "schema",
                }
            )

        if meta.get("format") == "email":
            constraints.append(
                {
                    "id": f"email_{path.replace('.', '_')}",
                    "field": path,
                    "kind": "response-property",
                    "rule": f"Field '{path}' must look like an email.",
                    "type": "email",
                    "confirmed": True,
                    "source": "schema",
                }
            )

    return constraints


def merge_constraints(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for group in groups:
        for item in group:
            key = (item.get("field", ""), item.get("type", ""))
            if key not in merged:
                merged[key] = item
    return list(merged.values())
