from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine (Supabase pooler compatible)
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=None,              # ❗ Disable SQLAlchemy pooling (important)
    pool_pre_ping=True,          # Helps avoid stale connections
    connect_args={
        "sslmode": "require"     # Required for Supabase
    }
)

# Test DB connection once
try:
    with engine.connect() as conn:
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