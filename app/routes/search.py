from fastapi import APIRouter
from app.database import SessionLocal
from app.utils.embedder import get_embedding

router = APIRouter()

@router.post("/search")
def search_candidates(payload: dict):
    requirement = payload["requirement"]

    query_vec = get_embedding(requirement)

    db = SessionLocal()

    sql = """
    SELECT name, email, skills, experience,
           embedding <=> :query_vec AS distance
    FROM candidates
    ORDER BY distance ASC
    LIMIT 10;
    """

    rows = db.execute(sql, {"query_vec": query_vec}).fetchall()
    db.close()

    return [dict(r) for r in rows]
