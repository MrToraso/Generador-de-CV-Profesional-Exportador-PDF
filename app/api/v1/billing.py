from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.user import PlanType, User
from app.schemas.plan import CheckoutResponse, PlanResponse
from app.services.billing import (
    construct_webhook_event,
    create_or_get_customer,
    create_premium_checkout_session,
)
from app.utils.limits import max_analyses_by_plan

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/checkout/premium", response_model=CheckoutResponse)
def premium_checkout(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CheckoutResponse:
    customer_id = create_or_get_customer(user)
    if user.stripe_customer_id != customer_id:
        user.stripe_customer_id = customer_id
        db.add(user)
        db.commit()

    checkout_url = create_premium_checkout_session(customer_id=customer_id, user_id=user.id)
    return CheckoutResponse(checkout_url=checkout_url)


@router.post("/webhook", response_model=PlanResponse)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default="", alias="Stripe-Signature"),
    db: Session = Depends(get_db),
) -> PlanResponse:
    if not settings.stripe_webhook_secret or not settings.stripe_secret_key:
        raise HTTPException(status_code=500, detail="Stripe webhook no configurado")

    payload = await request.body()

    try:
        event = construct_webhook_event(payload, stripe_signature)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Webhook inválido: {exc}") from exc

    if event["type"] != "checkout.session.completed":
        raise HTTPException(status_code=202, detail="Evento ignorado")

    session_object = event["data"]["object"]
    user_id = session_object.get("metadata", {}).get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Webhook sin user_id")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.plan = PlanType.PREMIUM
    db.add(user)
    db.commit()

    return PlanResponse(current_plan=user.plan, analysis_limit=max_analyses_by_plan(user.plan))
