import re

from pidog_brain.planner.schema import AllowedAction, RobotAction, RobotPlan

_ACTION_ALIASES = {
    "sit": AllowedAction.sit,
    "sit down": AllowedAction.sit,
    "stand": AllowedAction.stand,
    "stand up": AllowedAction.stand,
    "rest": AllowedAction.rest,
    "lie down": AllowedAction.rest,
    "nod": AllowedAction.nod,
    "nod your head": AllowedAction.nod,
    "shake head": AllowedAction.shake_head,
    "shake your head": AllowedAction.shake_head,
    "wag tail": AllowedAction.wag_tail,
    "wag your tail": AllowedAction.wag_tail,
    "bark": AllowedAction.bark,
    "howl": AllowedAction.howl,
    "stretch": AllowedAction.stretch,
    "step forward": AllowedAction.step_forward,
    "move forward": AllowedAction.step_forward,
    "walk forward": AllowedAction.step_forward,
    "go forward": AllowedAction.step_forward,
    "step backward": AllowedAction.step_backward,
    "move backward": AllowedAction.step_backward,
    "go backward": AllowedAction.step_backward,
    "back up": AllowedAction.step_backward,
    "turn left": AllowedAction.turn_left,
    "turn right": AllowedAction.turn_right,
}

_STOP_COMMANDS = {"stop", "stop now", "please stop", "halt", "freeze", "emergency stop"}
_GREETINGS = {"hello", "hi", "hey", "say hello"}
_POLITE_PREFIX = re.compile(
    r"^(?:please\s+|can you\s+|could you\s+|would you\s+|will you\s+)+",
    re.IGNORECASE,
)
_CLAUSE_SPLIT = re.compile(r"\s+(?:and|then)\s+|\s*,\s*", re.IGNORECASE)


def _normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[.!?]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def route_fast_command(user_input: str) -> RobotPlan | None:
    normalized = _normalize(user_input)
    if not normalized:
        return None

    if normalized in _STOP_COMMANDS:
        return RobotPlan(
            say="Stopping.",
            actions=[RobotAction(name=AllowedAction.stop, duration_s=0.1)],
        )

    if normalized in _GREETINGS:
        return RobotPlan(say="Hello!", actions=[])

    clauses = _CLAUSE_SPLIT.split(user_input.strip())
    actions: list[RobotAction] = []
    speech = ""

    for original_clause in clauses:
        clause = _normalize(_POLITE_PREFIX.sub("", original_clause.strip()))
        if not clause or re.match(r"^(?:do not|don't|never|not)\b", clause):
            return None

        if clause.startswith("say "):
            spoken = _POLITE_PREFIX.sub("", original_clause.strip())[4:].strip()
            if not spoken:
                return None
            speech = spoken
            continue

        action = _ACTION_ALIASES.get(clause)
        if action is None:
            return None
        actions.append(RobotAction(name=action, duration_s=1.0))

    if not actions and not speech:
        return None
    return RobotPlan(say=speech or "Okay.", actions=actions)
