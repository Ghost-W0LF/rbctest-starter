from __future__ import annotations

import json
import os
from typing import Any

from groq import Groq


def _fallback_constraints(schema: dict[str, Any], required_fields: list[str]) -> list[dict[str, Any]]:
    constraints: list[dict[str, Any]] = []
    props = schema.get("properties", {})

    for field in required_fields:
        constraints.append(
            {
                "id": f"required_{field}",
                "field": field,
                "kind": "response-property",
                "rule": f"Field '{field}' must exist in response.",
                "type": "required",
                "confirmed": True,
            }
        )

    for field, meta in props.items():
        field_type = meta.get("type")
        if field_type in {"string", "integer", "number", "boolean", "object", "array"}:
            constraints.append(
                {
                    "id": f"type_{field}",
                    "field": field,
                    "kind": "response-property",
                    "rule": f"Field '{field}' must be of type '{field_type}'.",
                    "type": "type",
                    "expected_type": field_type,
                    "confirmed": True,
                }
            )
        if "enum" in meta:
            constraints.append(
                {
                    "id": f"enum_{field}",
                    "field": field,
                    "kind": "response-property",
                    "rule": f"Field '{field}' must be one of allowed enum values.",
                    "type": "enum",
                    "allowed_values": meta["enum"],
                    "confirmed": True,
                }
            )
        if meta.get("format") == "email":
            constraints.append(
                {
                    "id": f"format_email_{field}",
                    "field": field,
                    "kind": "response-property",
                    "rule": f"Field '{field}' must look like an email.",
                    "type": "email",
                    "confirmed": True,
                }
            )

    return constraints


def mine_constraints_with_oc(
    schema: dict[str, Any], required_fields: list[str], model: str = "llama-3.3-70b-versatile"
) -> tuple[list[dict[str, Any]], str]:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return _fallback_constraints(schema, required_fields), "fallback(no_api_key)"

    client = Groq(api_key=api_key)
    observation_prompt = f"""
You are mining response-body test constraints from an OpenAPI response schema.
Only output rules that are grounded in this schema.

Schema JSON:
{json.dumps(schema, indent=2)}

Required fields:
{json.dumps(required_fields)}

Return ONLY valid JSON array. Each item must contain:
- id
- field
- kind (response-property)
- rule (natural language)
- type (one of: required, type, enum, email)
- expected_type (only for type)
- allowed_values (only for enum)
"""

    observation = client.chat.completions.create(
        model=model,
        max_tokens=1600,
        temperature=0,
        messages=[{"role": "user", "content": observation_prompt}],
    )
    raw = (observation.choices[0].message.content or "").strip()
    proposed = _parse_json_array(raw)

    confirmation_prompt = f"""
You are validating proposed API constraints. For each constraint, decide if it is
strictly supported by the schema. Reject unsupported ones.

Schema JSON:
{json.dumps(schema, indent=2)}

Proposed constraints:
{json.dumps(proposed, indent=2)}

Return ONLY valid JSON array with:
- id
- confirmed (true/false)
- reason (short)
"""
    confirmation = client.chat.completions.create(
        model=model,
        max_tokens=1400,
        temperature=0,
        messages=[{"role": "user", "content": confirmation_prompt}],
    )
    checks = _parse_json_array((confirmation.choices[0].message.content or "").strip())
    confirmed_map = {c["id"]: c for c in checks if c.get("confirmed") is True}

    confirmed_constraints: list[dict[str, Any]] = []
    for item in proposed:
        check = confirmed_map.get(item.get("id"))
        if check:
            item["confirmed"] = True
            item["reason"] = check.get("reason", "")
            confirmed_constraints.append(item)

    if not confirmed_constraints:
        return _fallback_constraints(schema, required_fields), "fallback(confirmation_empty)"

    return confirmed_constraints, f"llm({model})"


def _parse_json_array(text: str) -> list[dict[str, Any]]:
    text = text.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    data = json.loads(text.strip())
    if not isinstance(data, list):
        raise ValueError("Expected JSON array from LLM.")
    return data
