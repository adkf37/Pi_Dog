from pidog_brain.planner.router import route_fast_command
from pidog_brain.planner.schema import AllowedAction


def test_routes_single_action():
    plan = route_fast_command("please sit down")
    assert plan is not None
    assert plan.actions[0].name == AllowedAction.sit


def test_routes_speech_and_action():
    plan = route_fast_command("say Hello Aaron and wag your tail")
    assert plan is not None
    assert plan.say == "Hello Aaron"
    assert plan.actions[0].name == AllowedAction.wag_tail


def test_routes_stop_as_immediate_action():
    plan = route_fast_command("emergency stop")
    assert plan is not None
    assert plan.actions[0].name == AllowedAction.stop
    assert plan.actions[0].duration_s == 0.1


def test_unknown_command_falls_back_to_llm():
    assert route_fast_command("act excited because my friend arrived") is None


def test_negated_command_does_not_execute():
    assert route_fast_command("don't sit") is None


def test_partial_match_does_not_execute():
    assert route_fast_command("sit near the doorway") is None
