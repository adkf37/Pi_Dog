import json

from pidog_brain.planner.schema import AllowedAction

SYSTEM_PROMPT = """Plan a safe response for a small robot dog.
Return only JSON. Never invent actions, servo commands, or code."""


def build_prompt(
    user_input: str,
    robot_state: dict | None = None,
    *,
    max_actions: int = 3,
    max_duration: float = 3.0,
) -> str:
    allowed = ",".join(action.value for action in AllowedAction)
    parts = [SYSTEM_PROMPT]
    parts.append(f"Actions: {allowed}.")
    parts.append(
        f"Use at most {max_actions} actions; duration_s must be >0 and <={max_duration:g}s. "
        'Shape: {"say":"short reply","actions":[{"name":"sit","duration_s":1}]}.'
    )
    if robot_state:
        parts.append(f"State: {json.dumps(robot_state, separators=(',', ':'))}")
    parts.append(f"Request: {user_input}")
    return "\n".join(parts)
