import asyncio
import time

from pidog_brain.llm.base import LLMBase
from pidog_brain.planner import Planner
from pidog_brain.planner.schema import AllowedAction
from pidog_brain.runtime import AsyncPlannerRuntime


class SlowLLM(LLMBase):
    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str, **kwargs) -> str:
        self.calls += 1
        time.sleep(0.15)
        return '{"say": "done", "actions": []}'


def test_fast_command_does_not_call_background_llm():
    async def scenario() -> None:
        llm = SlowLLM()
        runtime = AsyncPlannerRuntime(
            Planner(llm, movement_enabled=True, fast_path_enabled=True)
        )
        try:
            plan = await runtime.plan("sit")
            assert plan.actions[0].name == AllowedAction.sit
            assert llm.calls == 0
        finally:
            runtime.close()

    asyncio.run(scenario())


def test_stop_bypasses_in_flight_llm_and_supersedes_stale_plan():
    async def scenario() -> None:
        llm = SlowLLM()
        runtime = AsyncPlannerRuntime(
            Planner(llm, movement_enabled=True, fast_path_enabled=True)
        )
        try:
            pending = asyncio.create_task(runtime.plan("do something surprising"))
            await asyncio.sleep(0.02)
            started = time.perf_counter()
            stop_plan = await runtime.plan("stop")
            elapsed = time.perf_counter() - started

            assert elapsed < 0.05
            assert stop_plan.actions[0].name == AllowedAction.stop
            stale_plan = await pending
            assert stale_plan.actions == []
            assert stale_plan.say == ""
        finally:
            runtime.close()

    asyncio.run(scenario())
