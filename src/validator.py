from __future__ import annotations

import re
from typing import Any


def validate_constraints(response_json: dict[str, Any], constraints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for c in constraints:
        ctype = c.get("type")
        field = c.get("field")
        value = response_json.get(field)
        ok = True
        detail = "pass"

        if ctype == "required":
            ok = field in response_json
            if not ok:
                detail = f"missing field '{field}'"
        elif ctype == "type":
            expected = c.get("expected_type")
            ok = _matches_type(value, expected)
            if not ok:
                detail = f"expected {expected}, got {type(value).__name__}"
        elif ctype == "enum":
            allowed = c.get("allowed_values", [])
            ok = value in allowed
            if not ok:
                detail = f"value '{value}' not in enum {allowed}"
        elif ctype == "email":
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
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "object": dict,
        "array": list,
    }
    py_type = type_map.get(expected)
    if py_type is None:
        return False
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, py_type)
