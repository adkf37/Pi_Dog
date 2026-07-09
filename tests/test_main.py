from unittest.mock import patch

from pidog_brain.main import _format_summary, _build_llm, _build_robot
from pidog_brain.config import Settings
from pidog_brain.planner.schema import RobotPlan, AllowedAction, RobotAction


def test_format_summary() -> None:
    actions = [RobotAction(name=AllowedAction.sit, duration_s=1.0)]
    summary = _format_summary(
        mode="mock",
        model="tinyllama",
        user_input="say hello",
        latency=1.23,
        speech="Hello!",
        actions=actions,
    )
    assert "mock" in summary
    assert "tinyllama" in summary
    assert "say hello" in summary
    assert "1.23s" in summary
    assert "Hello!" in summary
    assert "sit" in summary


def test_format_summary_empty_actions() -> None:
    summary = _format_summary(
        mode="mock",
        model="tinyllama",
        user_input="",
        latency=0.5,
        speech="",
        actions=[],
    )
    assert "Actions:      0" in summary


def test_build_llm_ollama() -> None:
    settings = Settings(llm_backend="ollama")
    llm = _build_llm(settings)
    from pidog_brain.llm.ollama_client import OllamaClient
    assert isinstance(llm, OllamaClient)
    assert llm.host == "http://localhost:11434"
    assert llm.model == "tinyllama"


def test_build_llm_llamacpp() -> None:
    settings = Settings(llm_backend="llama.cpp", llama_model_path="/fake/path.gguf")
    llm = _build_llm(settings)
    from pidog_brain.llm.llama_cpp_client import LlamaCppClient
    assert isinstance(llm, LlamaCppClient)
    assert llm.model_path == "/fake/path.gguf"


def test_build_robot_mock() -> None:
    robot = _build_robot("mock")
    from pidog_brain.robot.mock_robot import MockRobot
    assert isinstance(robot, MockRobot)


def test_main_runs_mock_mode() -> None:
    with (
        patch("pidog_brain.main.MockRobot.execute") as mock_execute,
        patch("pidog_brain.main.Planner.plan") as mock_plan,
    ):
        mock_plan.return_value = RobotPlan(
            say="hello world",
            actions=[RobotAction(name=AllowedAction.sit, duration_s=1.0)],
        )
        mock_execute.return_value = {
            "speech": "hello world",
            "actions": [{"action": "sit", "duration_s": 1.0, "status": "executed"}],
        }

        from pidog_brain.main import main
        import sys
        sys.argv = ["pidog_brain.main", "--mode", "mock", "--input", "hello"]
        main()

        mock_plan.assert_called_once()
        assert "hello" in mock_plan.call_args[0][0]
        mock_execute.assert_called_once_with(mock_plan.return_value)


def test_main_defaults_to_say_hello() -> None:
    with (
        patch("pidog_brain.main.MockRobot.execute") as mock_execute,
        patch("pidog_brain.main.Planner.plan") as mock_plan,
    ):
        mock_plan.return_value = RobotPlan(say="hi", actions=[])
        mock_execute.return_value = {"speech": "hi", "actions": []}

        from pidog_brain.main import main
        import sys
        sys.argv = ["pidog_brain.main", "--mode", "mock"]
        main()

        mock_plan.assert_called_once()
        assert "say hello" in mock_plan.call_args[0][0]


def test_main_bench_mode_disables_movement() -> None:
    with (
        patch("pidog_brain.main.MockRobot.execute") as mock_execute,
        patch("pidog_brain.main.Planner") as MockPlanner,
    ):
        mock_planner_instance = MockPlanner.return_value
        mock_planner_instance.plan.return_value = RobotPlan(say="ok", actions=[])
        mock_execute.return_value = {"speech": "ok", "actions": []}

        from pidog_brain.main import main
        import sys
        sys.argv = ["pidog_brain.main", "--mode", "mock", "--bench"]
        main()

        assert MockPlanner.called
        _, kwargs = MockPlanner.call_args
        assert kwargs.get("movement_enabled") is False


def test_main_empty_input_default() -> None:
    with (
        patch("pidog_brain.main.MockRobot.execute") as mock_execute,
        patch("pidog_brain.main.Planner.plan") as mock_plan,
    ):
        mock_plan.return_value = RobotPlan(say="hi", actions=[])
        mock_execute.return_value = {"speech": "hi", "actions": []}

        from pidog_brain.main import main
        import sys
        sys.argv = ["pidog_brain.main", "--mode", "mock", "--input", ""]
        main()

        mock_plan.assert_called_once()
        assert "say hello" in mock_plan.call_args[0][0]
