from app.models.user import PlanType

FREE_PLAN_ANALYSIS_LIMIT = 3


def max_analyses_by_plan(plan: PlanType) -> int | None:
    if plan == PlanType.FREE:
        return FREE_PLAN_ANALYSIS_LIMIT
    return None
