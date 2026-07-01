import pytest

from pidog_brain.planner.schema import RobotPlan, RobotAction
from pidog_brain.planner.policy import validate_plan, PolicyViolation


def make_plan(*actions) -> RobotPlan:
    return RobotPlan(actions=[RobotAction(name=n, duration_s=d) for n, d in actions])


def test_valid_plan_passes():
    plan = make_plan(("sit", 1.0), ("wag_tail", 2.0))
    result = validate_plan(plan, movement_enabled=True)
    assert len(result.actions) == 2


def test_too_many_actions_rejected():
    plan = make_plan(
        ("sit", 1.0), ("stand", 1.0), ("nod", 1.0), ("bark", 1.0),
    )
    with pytest.raises(PolicyViolation, match="exceeds max"):
        validate_plan(plan, movement_enabled=True, max_actions=3)


def test_movement_blocked_in_bench_mode():
    plan = make_plan(("sit", 1.0), ("step_forward", 1.0))
    with pytest.raises(PolicyViolation, match="blocked in bench mode"):
        validate_plan(plan, movement_enabled=False)


def test_movement_allowed_when_enabled():
    plan = make_plan(("step_forward", 1.0), ("turn_left", 1.0))
    result = validate_plan(plan, movement_enabled=True)
    assert len(result.actions) == 2


def test_duration_clamped():
    plan = make_plan(("sit", 10.0))
    result = validate_plan(plan, movement_enabled=True, max_duration=3.0)
    assert result.actions[0].duration_s == 3.0


def test_empty_plan_passes():
    plan = RobotPlan()
    result = validate_plan(plan, movement_enabled=False)
    assert result.actions == []


def test_invalid_action_rejected_by_schema():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        RobotAction(name="fly", duration_s=1.0)
