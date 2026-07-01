from pidog_brain.planner.schema import RobotPlan, AllowedAction, MOVEMENT_ACTIONS


class PolicyViolation(ValueError):
    pass


def validate_plan(plan: RobotPlan, movement_enabled: bool, max_actions: int = 3, max_duration: float = 3.0) -> RobotPlan:
    if not plan.actions:
        return plan

    if len(plan.actions) > max_actions:
        raise PolicyViolation(
            f"Plan has {len(plan.actions)} actions, exceeds max of {max_actions}"
        )

    validated: list = []
    for action in plan.actions:
        if not movement_enabled and action.name in MOVEMENT_ACTIONS:
            raise PolicyViolation(
                f"Movement action '{action.name.value}' is blocked in bench mode"
            )
        clamped_duration = min(action.duration_s, max_duration)
        if clamped_duration != action.duration_s:
            action.duration_s = clamped_duration
        validated.append(action)

    plan.actions = validated
    return plan
