from abc import ABC, abstractmethod

from pidog_brain.planner.schema import RobotPlan


class RobotBase(ABC):
    @abstractmethod
    def execute(self, plan: RobotPlan) -> dict:
        ...
