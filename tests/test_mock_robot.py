from pidog_brain.robot.mock_robot import MockRobot
from pidog_brain.planner.schema import RobotPlan, RobotAction


def test_mock_robot_executes_actions():
    robot = MockRobot()
    plan = RobotPlan(
        say="hello",
        actions=[
            RobotAction(name="sit", duration_s=1.0),
            RobotAction(name="wag_tail", duration_s=2.0),
        ],
    )
    result = robot.execute(plan)
    assert result["speech"] == "hello"
    assert len(result["actions"]) == 2
    assert len(robot.action_log) == 2
    assert robot.action_log[0]["action"] == "sit"
    assert robot.action_log[1]["action"] == "wag_tail"


def test_mock_robot_empty_plan():
    robot = MockRobot()
    plan = RobotPlan()
    result = robot.execute(plan)
    assert result["actions"] == []


def test_mock_robot_all_actions():
    robot = MockRobot()
    from pidog_brain.planner.schema import AllowedAction
    actions = [RobotAction(name=a, duration_s=0.5) for a in AllowedAction]
    plan = RobotPlan(actions=actions)
    result = robot.execute(plan)
    assert len(result["actions"]) == 14
