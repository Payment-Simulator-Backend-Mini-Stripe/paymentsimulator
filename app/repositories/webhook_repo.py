from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.webhook import WebhookConfig, WebhookLog

class WebhookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_webhook_config(self, merchant_id: int, url: str, secret: str) -> WebhookConfig:
        config = WebhookConfig(merchant_id=merchant_id, url=url, secret=secret)
        self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def get_webhook_config_by_merchant_id(self, merchant_id: int) -> WebhookConfig | None:
        result = await self.db.execute(
            select(WebhookConfig).where(WebhookConfig.merchant_id == merchant_id)
        )
        return result.scalar_one_or_none()

    async def create_webhook_log(self, payment_id: int, url: str, payload: str, status_code: int, success: bool, attempt: int) -> WebhookLog:
        log = WebhookLog(
            payment_id=payment_id,
            url=url,
            payload=payload,
            status_code=status_code,
            success=success,
            attempt=attempt
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log