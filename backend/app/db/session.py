import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# -----------------------------
# Database connection setup
# -----------------------------

# Retry loop for network issues
max_retries = 5
for attempt in range(max_retries):
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            # ✅ Connection pool settings safe for free Supabase
            pool_size=2,         # Max 2 persistent connections
            max_overflow=0,      # No extra connections beyond pool
            pool_timeout=30,     # Wait 30s for a free connection
            pool_pre_ping=True,  # Check connection before using
            connect_args={
                "sslmode": "require",        # Required by Supabase
                "connect_timeout": 10        # 10s timeout for initial connection
            }
        )

        # Test DB connection
        conn = engine.connect()
        conn.close()
        print("✅ Database connected successfully")
        break

    except Exception as e:
        print(f"[DB ERROR] {e}, retrying in 5s... ({attempt+1}/{max_retries})")
        time.sleep(5)
else:
    raise Exception(f"❌ Could not connect to database after {max_retries} attempts")

# -----------------------------
# SQLAlchemy session setup
# -----------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False  # Optional: keeps objects accessible after commit
)

# -----------------------------
# FastAPI dependency
# -----------------------------

def get_db():
    """
    Dependency for FastAPI routes to get a database session
    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()