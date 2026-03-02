from pydantic import BaseModel

from app.models.user import PlanType


class PlanUpgradeRequest(BaseModel):
    plan: PlanType


class PlanResponse(BaseModel):
    current_plan: PlanType
    analysis_limit: int | None


class CheckoutResponse(BaseModel):
    checkout_url: str
