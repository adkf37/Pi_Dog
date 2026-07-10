import asyncio
from concurrent.futures import ThreadPoolExecutor

from pidog_brain.planner import Planner
from pidog_brain.planner.schema import RobotPlan


class AsyncPlannerRuntime:
    """Keeps blocking LLM inference off the event loop and discards stale plans."""

    def __init__(self, planner: Planner):
        self._planner = planner
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="pidog-llm")
        self._request_id = 0

    async def plan(
        self,
        user_input: str,
        robot_state: dict | None = None,
    ) -> RobotPlan:
        self._request_id += 1
        request_id = self._request_id

        fast_plan = self._planner.plan_fast(user_input)
        if fast_plan is not None:
            return fast_plan

        loop = asyncio.get_running_loop()
        plan = await loop.run_in_executor(
            self._executor,
            self._planner.plan_with_llm,
            user_input,
            robot_state,
        )
        if request_id != self._request_id:
            return RobotPlan()
        return plan

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)
