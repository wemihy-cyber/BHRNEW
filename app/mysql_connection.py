# app/mysql_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

if not (MYSQL_HOST and MYSQL_DB and MYSQL_USER and MYSQL_PASSWORD):
    # If any missing, raise to avoid silent failure
    raise RuntimeError("MySQL credentials missing in environment variables.")

# Use pymysql dialect
MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

# create engine and session factory
mysql_engine = create_engine(MYSQL_URL, pool_pre_ping=True)
MySQLSessionLocal = sessionmaker(bind=mysql_engine, autocommit=False, autoflush=False)
