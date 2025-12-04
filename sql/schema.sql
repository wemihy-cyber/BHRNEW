-- create pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- table
CREATE TABLE IF NOT EXISTS candidates (
  id serial PRIMARY KEY,
  name text,
  resume_text text,
  resume_url text,
  embedding vector(1536),
  created_at timestamptz DEFAULT now()
);

-- ivfflat index for ANN (adjust lists param as needed)
CREATE INDEX IF NOT EXISTS candidates_embedding_ivfflat_idx
  ON candidates USING ivfflat (embedding) WITH (lists = 100);

ANALYZE candidates;
