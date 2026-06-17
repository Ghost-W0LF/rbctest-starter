from __future__ import annotations

import re
from typing import Any

_SEGMENT_RE = re.compile(r"^([^[]+)(?:\[(\d+)\])?$")


def get_value_by_path(data: dict[str, Any], field_path: str) -> tuple[bool, Any]:
    current: Any = data
    for part in field_path.split("."):
        if not part:
            return False, None

        match = _SEGMENT_RE.match(part)
        if not match:
            return False, None

        key = match.group(1)
        index = match.group(2)

        if not isinstance(current, dict) or key not in current:
            return False, None
        current = current[key]

        if index is not None:
            if not isinstance(current, list):
                return False, None
            idx = int(index)
            if idx < 0 or idx >= len(current):
                return False, None
            current = current[idx]

    return True, current


def validate_constraints(response_json: dict[str, Any], constraints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for c in constraints:
        ctype = c.get("type")
        field = c.get("field", "")
        ok = True
        detail = "pass"

        if ctype == "required":
            ok, _ = get_value_by_path(response_json, field)
            if not ok:
                detail = f"missing field '{field}'"
        elif ctype == "type":
            exists, value = get_value_by_path(response_json, field)
            if not exists:
                ok = False
                detail = f"missing field '{field}'"
            elif value is None and c.get("nullable"):
                ok = True
            else:
                expected = c.get("expected_type")
                ok = _matches_type(value, expected)
                if not ok:
                    detail = f"expected {expected}, got {type(value).__name__} (value={value!r})"
        elif ctype == "enum":
            exists, value = get_value_by_path(response_json, field)
            if not exists:
                ok = False
                detail = f"missing field '{field}'"
            elif value is None and c.get("nullable"):
                ok = True
            else:
                allowed = c.get("allowed_values", [])
                ok = value in allowed
                if not ok:
                    detail = f"value '{value}' not in enum {allowed}"
        elif ctype == "email":
            exists, value = get_value_by_path(response_json, field)
            if not exists:
                ok = False
                detail = f"missing field '{field}'"
            elif value is None and c.get("nullable"):
                ok = True
            else:
                ok = isinstance(value, str) and bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))
                if not ok:
                    detail = f"invalid email format: {value}"
        else:
            detail = f"unsupported constraint type '{ctype}'"

        results.append(
            {
                "id": c.get("id"),
                "field": field,
                "rule": c.get("rule"),
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    return results


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    type_map = {
        "string": str,
        "boolean": bool,
        "object": dict,
        "array": list,
    }
    py_type = type_map.get(expected)
    if py_type is None:
        return False
    return isinstance(value, py_type)
