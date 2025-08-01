from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.settings import Settings

settings = Settings()

engine = create_async_engine(settings.database_url, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session 
