from pidog_brain.planner.schema import AllowedAction
from pidog_brain.robot.actions import ACTION_DESCRIPTIONS

SYSTEM_PROMPT = """\
You are the planning brain for a small Raspberry Pi robot dog.
You must respond only with JSON matching the provided schema.
You may choose only from the allowed action list.
Do not invent actions.
Do not describe servo angles.
Do not write code.
Keep action sequences short and safe.
"""


def _action_schema_description() -> str:
    lines = ["Allowed actions and their descriptions:"]
    for action in AllowedAction:
        desc = ACTION_DESCRIPTIONS.get(action.value, "")
        lines.append(f"  - {action.value}: {desc}")
    lines.append("")
    lines.append(
        "Respond with JSON in the following format (no markdown fences):"
    )
    lines.append("""\
{
  "say": "What the robot says aloud",
  "actions": [
    {"name": "action_name", "duration_s": 1.0}
  ]
}""")
    lines.append("")
    lines.append(
        "Constraints:\n"
        f"  - 'name' must be one of: {', '.join(a.value for a in AllowedAction)}\n"
        "  - 'duration_s' must be a positive number (max 3.0)\n"
        "  - Maximum 3 actions per response\n"
        "  - If the user input implies nothing to do, respond with an empty actions list"
    )
    return "\n".join(lines)


def build_prompt(user_input: str, robot_state: dict | None = None) -> str:
    parts = [SYSTEM_PROMPT.strip()]
    parts.append("")
    parts.append(_action_schema_description())
    if robot_state:
        parts.append("")
        parts.append("Current robot state:")
        for key, value in robot_state.items():
            parts.append(f"  {key}: {value}")
    parts.append("")
    parts.append(f"User request: {user_input}")
    return "\n".join(parts)
