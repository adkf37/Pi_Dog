import argparse
import logging
import time

from pidog_brain.config import Settings, get_settings
from pidog_brain.llm import OllamaClient, LlamaCppClient
from pidog_brain.planner import Planner
from pidog_brain.robot.mock_robot import MockRobot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pidog_brain")


def _build_llm(settings: Settings) -> OllamaClient | LlamaCppClient:
    if settings.llm_backend == "ollama":
        logger.info(
            "Initializing Ollama client — host=%s model=%s",
            settings.ollama_host,
            settings.ollama_model,
        )
        return OllamaClient(host=settings.ollama_host, model=settings.ollama_model)
    if settings.llm_backend == "llama.cpp":
        logger.info("Initializing LlamaCpp client (stub)")
        return LlamaCppClient(model_path=settings.llama_model_path)
    raise ValueError(f"Unknown LLM backend: {settings.llm_backend}")


def _build_robot(mode: str) -> MockRobot:
    if mode == "robot":
        logger.warning(
            "Robot mode selected but PiDogAdapter is not yet implemented "
            "(task-09). Falling back to MockRobot."
        )
    return MockRobot()


def _format_summary(
    mode: str,
    model: str,
    user_input: str,
    latency: float,
    speech: str,
    actions: list,
) -> str:
    lines = [
        "=" * 50,
        "PiDog Brain — Demo Complete",
        "=" * 50,
        f"  Mode:         {mode}",
        f"  Model:        {model}",
        f"  Input:        {user_input}",
        f"  Latency:      {latency:.2f}s",
        f"  Speech:       {speech}",
        f"  Actions:      {len(actions)}",
    ]
    for action in actions:
        lines.append(f"    - {action.name.value} ({action.duration_s}s)")
    lines.append("=" * 50)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="PiDog Local LLM Brain")
    parser.add_argument(
        "--mode",
        choices=["mock", "robot"],
        default=None,
        help="Robot mode: mock (default) or robot (requires hardware)",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="",
        help="User input for the robot (default: 'say hello')",
    )
    parser.add_argument(
        "--bench",
        action="store_true",
        help="Enable bench mode (disables movement actions)",
    )
    args = parser.parse_args()

    settings: Settings = get_settings()
    if args.mode:
        settings.pidog_mode = args.mode
    if args.bench:
        settings.bench_mode = True

    user_input = args.input or "say hello"

    logger.info("PiDog Brain starting — mode=%s", settings.pidog_mode)
    logger.info("LLM backend=%s model=%s", settings.llm_backend, settings.ollama_model)
    logger.info("Movement enabled=%s", settings.movement_enabled)

    llm = _build_llm(settings)
    planner = Planner(llm, movement_enabled=settings.movement_enabled)

    logger.info("Planning for input: %s", user_input)
    start = time.perf_counter()

    parse_failure = False
    try:
        plan = planner.plan(user_input)
    except Exception:
        logger.exception("Unexpected error during planning")
        plan = None
        parse_failure = True

    latency = time.perf_counter() - start

    if plan is None:
        logger.error("Plan failed — no plan returned")
        print("Error: Failed to produce a plan. Check logs for details.")
        return

    logger.info(
        "Plan received in %.2fs — say=%s actions=%d",
        latency,
        plan.say,
        len(plan.actions),
    )

    robot = _build_robot(settings.pidog_mode)
    logger.info("Executing %d action(s)...", len(plan.actions))
    result = robot.execute(plan)
    logger.info(
        "Execution complete — speech=%s actions=%d",
        result.get("speech", ""),
        len(result.get("actions", [])),
    )

    print(
        _format_summary(
            mode=settings.pidog_mode,
            model=settings.ollama_model,
            user_input=user_input,
            latency=latency,
            speech=plan.say,
            actions=plan.actions,
        )
    )


if __name__ == "__main__":
    main()
