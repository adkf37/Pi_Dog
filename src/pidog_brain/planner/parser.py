import json
import re

from pidog_brain.planner.schema import RobotPlan


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _find_json_object(text: str) -> str | None:
    brace_depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == "{":
            if brace_depth == 0:
                start = i
            brace_depth += 1
        elif ch == "}":
            brace_depth -= 1
            if brace_depth == 0 and start >= 0:
                return text[start : i + 1]
    return None


def parse_llm_response(response: str) -> RobotPlan | None:
    cleaned = _strip_code_fences(response)

    obj = _find_json_object(cleaned)
    if not obj:
        return None

    try:
        data = json.loads(obj)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None

    safe = {"say": "", "actions": []}
    if isinstance(data.get("say"), str):
        safe["say"] = data["say"]

    raw_actions = data.get("actions")
    if isinstance(raw_actions, list):
        for item in raw_actions:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            duration = item.get("duration_s", 1.0)
            if name is None:
                continue
            safe["actions"].append({"name": name, "duration_s": duration})

    try:
        return RobotPlan(**safe)
    except Exception:
        return None
