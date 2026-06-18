from __future__ import annotations

import re
from typing import Any

from src.validator import get_value_by_path

_VALID_BRACKET_RE = re.compile(r"\[([^\]]*)\]")


def extract_schema_constraints(schema: dict[str, Any], prefix: str = "") -> list[dict[str, Any]]:
    """Deterministically mine type/required/email constraints from an OpenAPI schema."""
    constraints: list[dict[str, Any]] = []
    props = schema.get("properties", {})
    required_fields = set(schema.get("required", []))

    for name, meta in props.items():
        path = f"{prefix}.{name}" if prefix else name

        if name in required_fields:
            constraints.append(
                _constraint(
                    id_prefix="required",
                    path=path,
                    rule=f"Field '{path}' must exist in response.",
                    ctype="required",
                )
            )

        field_type = meta.get("type")
        if field_type == "object":
            constraints.extend(extract_schema_constraints(meta, path))
            continue

        if field_type == "array":
            constraints.append(
                _constraint(
                    id_prefix="type",
                    path=path,
                    rule=f"Field '{path}' must be of type 'array'.",
                    ctype="type",
                    expected_type="array",
                )
            )
            items = meta.get("items", {})
            if items.get("type") == "object":
                constraints.extend(extract_schema_constraints(items, f"{path}[*]"))
            continue

        if field_type in {"string", "integer", "number", "boolean"}:
            constraints.append(
                _constraint(
                    id_prefix="type",
                    path=path,
                    rule=f"Field '{path}' must be of type '{field_type}'.",
                    ctype="type",
                    expected_type=field_type,
                    nullable=bool(meta.get("nullable")),
                )
            )

        if "enum" in meta:
            constraints.append(
                _constraint(
                    id_prefix="enum",
                    path=path,
                    rule=f"Field '{path}' must be one of allowed enum values.",
                    ctype="enum",
                    allowed_values=meta["enum"],
                    nullable=bool(meta.get("nullable")),
                )
            )

        if meta.get("format") == "email":
            constraints.append(
                _constraint(
                    id_prefix="email",
                    path=path,
                    rule=f"Field '{path}' must look like an email.",
                    ctype="email",
                    nullable=bool(meta.get("nullable")),
                )
            )

    return drop_invalid_array_path_constraints(constraints)


def extract_downstream_constraints(schema: dict[str, Any], prefix: str = "") -> list[dict[str, Any]]:
    """Mine downstream-present oracles for nullable fields assumed non-null by consumers."""
    constraints: list[dict[str, Any]] = []
    props = schema.get("properties", {})

    for name, meta in props.items():
        path = f"{prefix}.{name}" if prefix else name
        field_type = meta.get("type")

        if field_type == "object":
            constraints.extend(extract_downstream_constraints(meta, path))
            continue

        if field_type == "array":
            items = meta.get("items", {})
            if items.get("type") == "object":
                constraints.extend(extract_downstream_constraints(items, f"{path}[*]"))
            continue

        if meta.get("nullable"):
            constraints.append(
                {
                    "id": f"downstream_{_path_id(path)}",
                    "field": path,
                    "kind": "response-property",
                    "rule": (
                        f"Downstream assumes '{path}' is present and non-null "
                        f"(spec marks it nullable)."
                    ),
                    "type": "downstream_present",
                    "confirmed": True,
                    "source": "downstream",
                }
            )

    return drop_invalid_array_path_constraints(constraints)


def expand_array_constraints(
    constraints: list[dict[str, Any]], response_json: dict[str, Any]
) -> list[dict[str, Any]]:
    """Expand [*] wildcard field paths into one constraint per array element."""
    expanded: list[dict[str, Any]] = []

    for constraint in constraints:
        field = constraint.get("field", "")
        if "[*]" not in field:
            expanded.append(constraint)
            continue

        array_path, suffix = field.split("[*]", maxsplit=1)
        exists, value = get_value_by_path(response_json, array_path)

        if not exists or not isinstance(value, list) or not value:
            expanded.append(_with_field(constraint, field.replace("[*]", "[0]"), 0))
            continue

        for index in range(len(value)):
            concrete_field = f"{array_path}[{index}]{suffix}"
            expanded.append(_with_field(constraint, concrete_field, index))

    return drop_invalid_array_path_constraints(expanded)


def drop_invalid_array_path_constraints(constraints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop constraints whose field paths use bare [] or other invalid bracket forms."""
    kept: list[dict[str, Any]] = []
    for constraint in constraints:
        field = constraint.get("field", "")
        if _is_valid_array_path(field):
            kept.append(constraint)
    return kept


def merge_constraints(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge constraint groups; later groups override earlier ones for the same field+type."""
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for group in groups:
        for item in group:
            key = (item.get("field", ""), item.get("type", ""))
            merged[key] = item
    return drop_invalid_array_path_constraints(list(merged.values()))


def dedupe_failures_by_field(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep at most one FAIL row per field path."""
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for row in results:
        if row.get("status") != "FAIL":
            continue
        field = row.get("field", "")
        if field in seen:
            continue
        seen.add(field)
        deduped.append(row)
    return deduped


def _is_valid_array_path(field: str) -> bool:
    if "[]" in field:
        return False
    for match in _VALID_BRACKET_RE.finditer(field):
        inner = match.group(1)
        if inner != "*" and not inner.isdigit():
            return False
    return True


def _constraint(
    id_prefix: str,
    path: str,
    rule: str,
    ctype: str,
    expected_type: str | None = None,
    allowed_values: list[Any] | None = None,
    nullable: bool = False,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": f"{id_prefix}_{_path_id(path)}",
        "field": path,
        "kind": "response-property",
        "rule": rule,
        "type": ctype,
        "confirmed": True,
        "source": "schema",
    }
    if expected_type is not None:
        item["expected_type"] = expected_type
    if allowed_values is not None:
        item["allowed_values"] = allowed_values
    if nullable:
        item["nullable"] = True
    return item


def _path_id(path: str) -> str:
    return path.replace(".", "_").replace("[*]", "_items").replace("[", "_").replace("]", "")


def _with_field(constraint: dict[str, Any], field: str, index: int) -> dict[str, Any]:
    updated = dict(constraint)
    updated["field"] = field
    base_id = constraint.get("id", "constraint")
    updated["id"] = f"{base_id}_{index}"
    return updated
