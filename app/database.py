import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Expect DATABASE_URL like: postgresql://user:pass@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bhrai")
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def ensure_pgvector_and_index(dim: int = 1536, lists: int = 100):
    """
    Ensure pgvector extension exists and create ivfflat index for 'candidates.embedding'.
    Call this once after migrations / table creation.
    """
    try:
        with engine.begin() as conn:
            # create extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            # create index (if table exists)
            # Note: SQLAlchemy won't auto-create this; do it manually here.
            conn.execute(text(f"""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'candidates') THEN
                    CREATE INDEX IF NOT EXISTS candidates_embedding_ivfflat_idx
                      ON candidates USING ivfflat (embedding) WITH (lists = {lists});
                    PERFORM pg_catalog.set_config('search_path', current_schema(), false);
                    EXECUTE 'ANALYZE candidates';
                END IF;
            END
            $$;
            """))
    except Exception as e:
        # log / ignore - important not to crash the whole app if DB temporarily unavailable
        print("Warning: ensure_pgvector_and_index failed:", e)
