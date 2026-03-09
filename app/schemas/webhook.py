from pydantic import BaseModel

class WebhookConfigCreate(BaseModel):
    url: str
    secret: str