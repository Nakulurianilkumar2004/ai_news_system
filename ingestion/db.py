from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Nanilkumar2004%40@db.bjlctgnnkjqfvfxndtmw.supabase.co:5432/postgres?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()