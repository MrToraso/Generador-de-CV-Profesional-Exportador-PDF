from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import PlanType, User
from app.schemas.plan import PlanResponse, PlanUpgradeRequest
from app.utils.limits import max_analyses_by_plan

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("/me", response_model=PlanResponse)
def my_plan(user: User = Depends(get_current_user)) -> PlanResponse:
    return PlanResponse(current_plan=user.plan, analysis_limit=max_analyses_by_plan(user.plan))


@router.post("/upgrade", response_model=PlanResponse)
def upgrade_plan(
    payload: PlanUpgradeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PlanResponse:
    user.plan = PlanType(payload.plan)
    db.add(user)
    db.commit()
    return PlanResponse(current_plan=user.plan, analysis_limit=max_analyses_by_plan(user.plan))
