import pytest
from pydantic import ValidationError

from pidog_brain.planner.schema import AllowedAction, RobotAction, RobotPlan


def test_allowed_action_enum_has_14_actions():
    assert len(AllowedAction) == 14


def test_valid_robot_action():
    action = RobotAction(name="sit", duration_s=1.5)
    assert action.name == AllowedAction.sit
    assert action.duration_s == 1.5


def test_invalid_action_name():
    with pytest.raises(ValidationError):
        RobotAction(name="fly", duration_s=1.0)


def test_negative_duration():
    with pytest.raises(ValidationError):
        RobotAction(name="sit", duration_s=-1.0)


def test_zero_duration():
    with pytest.raises(ValidationError):
        RobotAction(name="sit", duration_s=0)


def test_valid_robot_plan():
    plan = RobotPlan(
        say="hello",
        actions=[
            RobotAction(name="sit", duration_s=1.0),
            RobotAction(name="wag_tail", duration_s=2.0),
        ],
    )
    assert plan.say == "hello"
    assert len(plan.actions) == 2


def test_empty_plan():
    plan = RobotPlan()
    assert plan.say == ""
    assert plan.actions == []


def test_all_actions_accessible():
    names = {a.value for a in AllowedAction}
    expected = {
        "sit", "stand", "rest", "nod", "shake_head", "wag_tail",
        "bark", "howl", "stretch", "step_forward", "step_backward",
        "turn_left", "turn_right", "stop",
    }
    assert names == expected
