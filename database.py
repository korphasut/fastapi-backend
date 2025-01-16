import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Connection String (ลบ ?sslmode=require ออกจาก URL)
DATABASE_URL = "postgresql+asyncpg://automation_test_db_owner:eJc1ikzRTC6l@ep-billowing-haze-a1h4m12r.ap-southeast-1.aws.neon.tech/automation_test_db"

# สร้าง SSL Context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# สร้าง Async Engine พร้อม SSL
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"ssl": ssl_context})

# สร้าง SessionMaker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency สำหรับการสร้าง Session
async def get_db():
    async with async_session() as session:
        yield session
