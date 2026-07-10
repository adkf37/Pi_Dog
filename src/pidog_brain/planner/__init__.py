import logging

from pidog_brain.config import get_settings
from pidog_brain.llm.base import LLMBase
from pidog_brain.planner.parser import parse_llm_response
from pidog_brain.planner.policy import PolicyViolation, validate_plan
from pidog_brain.planner.prompts import build_prompt
from pidog_brain.planner.router import route_fast_command
from pidog_brain.planner.schema import RobotPlan

logger = logging.getLogger("pidog_brain.planner")


class Planner:
    def __init__(
        self,
        llm: LLMBase,
        movement_enabled: bool | None = None,
        fast_path_enabled: bool | None = None,
    ):
        self._llm = llm
        settings = get_settings()
        self._movement_enabled = (
            movement_enabled
            if movement_enabled is not None
            else settings.movement_enabled
        )
        self._max_actions = settings.max_actions_per_turn
        self._max_duration = settings.max_action_duration_s
        self._fast_path_enabled = (
            fast_path_enabled
            if fast_path_enabled is not None
            else settings.enable_fast_path
        )
        self.last_route = "none"

    def plan(self, user_input: str, robot_state: dict | None = None) -> RobotPlan:
        fast_plan = self.plan_fast(user_input)
        if fast_plan is not None:
            return fast_plan
        return self.plan_with_llm(user_input, robot_state)

    def plan_fast(self, user_input: str) -> RobotPlan | None:
        if not self._fast_path_enabled:
            return None
        plan = route_fast_command(user_input)
        if plan is None:
            return None
        self.last_route = "fast"
        return self._validate(plan)

    def plan_with_llm(
        self,
        user_input: str,
        robot_state: dict | None = None,
    ) -> RobotPlan:
        self.last_route = "llm"
        prompt = build_prompt(
            user_input,
            robot_state,
            max_actions=self._max_actions,
            max_duration=self._max_duration,
        )

        try:
            raw = self._llm.generate(prompt, format=RobotPlan.model_json_schema())
        except Exception as exc:
            self.last_route = "llm_error"
            logger.warning("LLM planning failed: %s", exc)
            return RobotPlan(
                say="I'm sorry, I couldn't reach my planning engine.",
                actions=[],
            )

        plan = parse_llm_response(raw)

        if plan is None:
            self.last_route = "llm_parse_error"
            return RobotPlan(
                say="I'm sorry, I couldn't understand my own response.",
                actions=[],
            )

        return self._validate(plan)

    def _validate(self, plan: RobotPlan) -> RobotPlan:
        try:
            return validate_plan(
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
