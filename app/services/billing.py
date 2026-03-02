from importlib import import_module
from typing import Any

from fastapi import HTTPException

from app.core.config import settings
from app.models.user import User


def _stripe_sdk() -> Any:
    try:
        return import_module("stripe")
    except ModuleNotFoundError as exc:
        raise HTTPException(status_code=500, detail="SDK de Stripe no instalado") from exc


def _configure_stripe() -> Any:
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=500, detail="Stripe no está configurado")
    stripe = _stripe_sdk()
    stripe.api_key = settings.stripe_secret_key
    return stripe


def create_or_get_customer(user: User) -> str:
    stripe = _configure_stripe()
    if user.stripe_customer_id:
        return user.stripe_customer_id
    customer = stripe.Customer.create(email=user.email, name=user.full_name, metadata={"user_id": user.id})
    return str(customer["id"])


def create_premium_checkout_session(customer_id: str, user_id: int) -> str:
    stripe = _configure_stripe()
    if not settings.stripe_premium_price_id:
        raise HTTPException(status_code=500, detail="Falta stripe_premium_price_id en configuración")

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": settings.stripe_premium_price_id, "quantity": 1}],
        success_url=settings.stripe_success_url,
        cancel_url=settings.stripe_cancel_url,
        metadata={"user_id": str(user_id), "target_plan": "premium"},
    )
    return str(session["url"])


def construct_webhook_event(payload: bytes, signature: str) -> Any:
    stripe = _configure_stripe()
    return stripe.Webhook.construct_event(payload, signature, settings.stripe_webhook_secret)
