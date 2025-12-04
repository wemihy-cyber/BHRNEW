from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from pgvector.sqlalchemy import Vector
from .database import Base

EMBED_DIM = 1536  # change to match your embedding dimensions

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True)
    resume_url = Column(Text, nullable=True)
    embedding = Column(Vector(EMBED_DIM), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
