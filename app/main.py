import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Absolute imports to use package layout
from app.database import SessionLocal, engine, Base
from app.models import Candidate
from app.utils.parser import extract_text_from_file
from app.utils.embedder import embed_text

load_dotenv()

API_KEY = os.getenv("API_KEY", "changeme")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/resumes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# create tables (won't create pgvector index; see database.py for index creation)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BHRAI Resume API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.post("/api/upload", dependencies=[Depends(check_api_key)])
async def upload_resume(file: UploadFile = File(...), name: str = Form(None), db: Session = Depends(get_db)):
    # save file
    file_ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid.uuid4().hex}{file_ext}"
    target = os.path.join(UPLOAD_DIR, fname)
    with open(target, "wb") as f:
        content = await file.read()
        f.write(content)

    text = extract_text_from_file(target, file.content_type)
    if not text:
        raise HTTPException(400, "Could not extract text from resume")

    emb = embed_text(text)

    candidate = Candidate(
        name=name,
        resume_text=text,
        resume_url=target,
        embedding=emb
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return {"id": candidate.id}


@app.post("/api/search", dependencies=[Depends(check_api_key)])
def search(q: str = Form(...), top_k: int = Form(10), db: Session = Depends(get_db)):
    qvec = embed_text(q)
    # raw SQL using pgvector cosine operator (<#> is cosine distance)
    sql = """
    SELECT id, name, resume_text, resume_url, embedding <#> :qvec as distance
    FROM candidates
    ORDER BY embedding <#> :qvec
    LIMIT :k;
    """
    # Using SQL text binding is fine; SQLAlchemy will pass list/array to pgvector adapter
    res = db.execute(sql, {"qvec": qvec, "k": top_k})
    rows = []
    for r in res:
        rows.append({
            "id": r.id,
            "name": r.name,
            "resume_text": (r.resume_text[:500] + "...") if r.resume_text else "",
            "resume_url": r.resume_url,
            "distance": float(r.distance)
        })
    return {"results": rows}


@app.get("/api/test")
def test():
    return {"status": "FastAPI running"}
