from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_validator


class AllowedAction(str, Enum):
    sit = "sit"
    stand = "stand"
    rest = "rest"
    nod = "nod"
    shake_head = "shake_head"
    wag_tail = "wag_tail"
    bark = "bark"
    howl = "howl"
    stretch = "stretch"
    step_forward = "step_forward"
    step_backward = "step_backward"
    turn_left = "turn_left"
    turn_right = "turn_right"
    stop = "stop"


MOVEMENT_ACTIONS = {
    AllowedAction.step_forward,
    AllowedAction.step_backward,
    AllowedAction.turn_left,
    AllowedAction.turn_right,
}


class RobotAction(BaseModel):
    name: AllowedAction
    duration_s: float = Field(gt=0, default=1.0)

    @field_validator("duration_s")
    @classmethod
    def duration_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("duration_s must be positive")
        return v


class RobotPlan(BaseModel):
    say: str = ""
    actions: List[RobotAction] = Field(default_factory=list)
