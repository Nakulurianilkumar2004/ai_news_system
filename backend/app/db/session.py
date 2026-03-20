from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=2,        # Free-tier safe
    max_overflow=0,
    pool_timeout=30,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    }
)

# Test DB connection once
try:
    conn = engine.connect()
    conn.close()
    print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Could not connect to database: {e}")
    raise e  # Fail startup immediately

# SQLAlchemy session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
    
# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()