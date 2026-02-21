from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
Base = declarative_base()
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)