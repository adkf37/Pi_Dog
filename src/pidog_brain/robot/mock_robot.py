import time

from pidog_brain.robot.base import RobotBase
from pidog_brain.planner.schema import RobotPlan, AllowedAction


class MockRobot(RobotBase):
    def __init__(self):
        self.action_log: list[dict] = []

    def execute(self, plan: RobotPlan) -> dict:
        results = []
        for action in plan.actions:
            entry = {
                "action": action.name.value,
                "duration_s": action.duration_s,
                "status": "executed",
            }
            print(f"[MockRobot] {action.name.value} for {action.duration_s}s")
            self.action_log.append(entry)
            results.append(entry)
            time.sleep(0.1)
        print(f"[MockRobot] Say: \"{plan.say}\"")
        return {"speech": plan.say, "actions": results}
