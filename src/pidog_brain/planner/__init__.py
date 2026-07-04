from pidog_brain.config import get_settings
from pidog_brain.llm.base import LLMBase
from pidog_brain.planner.parser import parse_llm_response
from pidog_brain.planner.policy import validate_plan, PolicyViolation
from pidog_brain.planner.prompts import build_prompt
from pidog_brain.planner.schema import RobotPlan


class Planner:
    def __init__(self, llm: LLMBase, movement_enabled: bool | None = None):
        self._llm = llm
        settings = get_settings()
        self._movement_enabled = (
            movement_enabled
            if movement_enabled is not None
            else settings.movement_enabled
        )
        self._max_actions = settings.max_actions_per_turn
        self._max_duration = settings.max_action_duration_s

    def plan(self, user_input: str, robot_state: dict | None = None) -> RobotPlan:
        prompt = build_prompt(user_input, robot_state)

        try:
            raw = self._llm.generate(prompt)
        except Exception:
            return RobotPlan(
                say="I'm sorry, I couldn't reach my planning engine.",
                actions=[],
            )

        plan = parse_llm_response(raw)

        if plan is None:
            return RobotPlan(
                say="I'm sorry, I couldn't understand my own response.",
                actions=[],
            )

        try:
            plan = validate_plan(
                plan,
                movement_enabled=self._movement_enabled,
                max_actions=self._max_actions,
                max_duration=self._max_duration,
            )
        except PolicyViolation:
            return RobotPlan(
                say="I planned something unsafe. Please try a simpler request.",
                actions=[],
            )

        return plan
