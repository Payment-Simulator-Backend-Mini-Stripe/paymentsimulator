import asyncio
import hmac
import hashlib
import json
import httpx 
from app.repositories.webhook_repo import WebhookRepository


class WebhookService:
    def __init__(self, webhook_repo: WebhookRepository):
        self.webhook_repo = webhook_repo

    def generate_signature(self, payload: str, secret: str) -> str:
        return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def verify_signature(self, payload: str, signature: str, secret: str) -> bool:
        expected_signature = self.generate_signature(payload, secret)
        return hmac.compare_digest(expected_signature, signature)

    async def send_webhook(self, payment):
        webhook_config = await self.webhook_repo.get_webhook_config_by_merchant_id(payment.payer_id)
        if not webhook_config:
            return

        payload = json.dumps({
    "content": f"Payment {payment.id} changed to {payment.status} - Amount: {payment.amount}"
        })
        signature = self.generate_signature(payload, webhook_config.secret)

        status_code = None
        response_body = None
        success = False


        for attempt in range(1, 4):

            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        webhook_config.url,
                        content=payload,
                        headers={
                            "Content-Type": "application/json",
                            "X-Webhook-Signature": signature,
                        },
                    )
                status_code = response.status_code
                response_body = response.text
                success = 200 <= response.status_code < 300
            except httpx.HTTPError as exc:
                response_body = str(exc)

            await self.webhook_repo.create_webhook_log(
                payment_id=payment.id,
                url=webhook_config.url,
                payload=payload,
                status_code=status_code,
                attempt=attempt,
                success=success,
            )
            if success:
                break

            if attempt < 3:
                 await asyncio.sleep(2 ** (attempt - 1))



