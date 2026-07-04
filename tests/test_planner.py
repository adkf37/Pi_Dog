from pidog_brain.llm.base import LLMBase
from pidog_brain.planner import Planner
from pidog_brain.planner.parser import parse_llm_response
from pidog_brain.planner.prompts import build_prompt
from pidog_brain.planner.schema import RobotPlan, AllowedAction


class MockLLM(LLMBase):
    def __init__(self, response: str = ""):
        self.response = response
        self.last_prompt: str = ""

    def generate(self, prompt: str, **kwargs) -> str:
        self.last_prompt = prompt
        return self.response


class RaisingLLM(LLMBase):
    def generate(self, prompt: str, **kwargs) -> str:
        raise RuntimeError("LLM unavailable")


def test_planner_returns_validated_plan():
    llm = MockLLM(
        response='{"say": "hello", "actions": [{"name": "sit", "duration_s": 1.0}]}'
    )
    planner = Planner(llm, movement_enabled=True)
    plan = planner.plan("sit down")
    assert isinstance(plan, RobotPlan)
    assert plan.say == "hello"
    assert len(plan.actions) == 1
    assert plan.actions[0].name == AllowedAction.sit


def test_planner_invalid_json_fallback():
    llm = MockLLM(response="this is not json")
    planner = Planner(llm, movement_enabled=True)
    plan = planner.plan("do something")
    assert isinstance(plan, RobotPlan)
    assert "couldn't understand" in plan.say.lower()
    assert plan.actions == []


def test_planner_policy_violation_fallback():
    llm = MockLLM(
        response='{"say": "", "actions": [{"name": "step_forward", "duration_s": 1.0}]}'
    )
    planner = Planner(llm, movement_enabled=False)
    plan = planner.plan("walk forward")
    assert isinstance(plan, RobotPlan)
    assert "unsafe" in plan.say.lower()
    assert plan.actions == []


def test_planner_llm_exception_fallback():
    llm = RaisingLLM()
    planner = Planner(llm, movement_enabled=True)
    plan = planner.plan("do something")
    assert isinstance(plan, RobotPlan)
    assert "couldn't reach" in plan.say.lower()
    assert plan.actions == []


def test_planner_sends_user_input_in_prompt():
    llm = MockLLM(response='{"say": "ok", "actions": []}')
    planner = Planner(llm, movement_enabled=True)
    planner.plan("wag tail")
    assert "wag tail" in llm.last_prompt


def test_planner_sends_robot_state_in_prompt():
    llm = MockLLM(response='{"say": "ok", "actions": []}')
    planner = Planner(llm, movement_enabled=True)
    planner.plan("hello", robot_state={"battery": 85, "mode": "mock"})
    assert "battery" in llm.last_prompt
    assert "85" in llm.last_prompt
    assert "mode" in llm.last_prompt


def test_planner_empty_input():
    llm = MockLLM(response='{"say": "", "actions": []}')
    planner = Planner(llm, movement_enabled=True)
    plan = planner.plan("")
    assert isinstance(plan, RobotPlan)
    assert plan.actions == []


def test_parse_llm_response_valid_json():
    result = parse_llm_response(
        '{"say": "hi", "actions": [{"name": "nod", "duration_s": 0.5}]}'
    )
    assert result is not None
    assert result.say == "hi"
    assert len(result.actions) == 1
    assert result.actions[0].name == AllowedAction.nod


def test_parse_llm_response_markdown_fences():
    result = parse_llm_response(
        '```json\n{"say": "hello", "actions": [{"name": "bark", "duration_s": 1.0}]}\n```'
    )
    assert result is not None
    assert result.say == "hello"
    assert result.actions[0].name == AllowedAction.bark


def test_parse_llm_response_markdown_fences_no_lang():
    result = parse_llm_response(
        '```\n{"say": "hello", "actions": []}\n```'
    )
    assert result is not None
    assert result.say == "hello"


def test_parse_llm_response_garbage():
    result = parse_llm_response("not json at all")
    assert result is None


def test_parse_llm_response_empty():
    result = parse_llm_response("")
    assert result is None


def test_parse_llm_response_partial_json():
    result = parse_llm_response(
        'Here is your plan: {"say": "ok", "actions": [{"name": "sit", "duration_s": 1.0}]}'
    )
    assert result is not None
    assert result.say == "ok"
    assert result.actions[0].name == AllowedAction.sit


def test_build_prompt_contains_action_list():
    prompt = build_prompt("say hello")
    for action in AllowedAction:
        assert action.value in prompt


def test_build_prompt_contains_user_input():
    prompt = build_prompt("wag tail twice")
    assert "wag tail twice" in prompt


def test_build_prompt_with_robot_state():
    prompt = build_prompt("hello", robot_state={"battery": 50})
    assert "battery" in prompt
    assert "50" in prompt


def test_build_prompt_without_robot_state():
    prompt = build_prompt("hello")
    assert "battery" not in prompt
