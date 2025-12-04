FROM python:3.11-slim

WORKDIR /app

# Install system deps (psycopg2 build deps, pdftotext via poppler-utils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV UPLOAD_DIR=/tmp/resumes
RUN mkdir -p ${UPLOAD_DIR}

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
