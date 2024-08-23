from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.env import envConfig
DATABASE_URL=f"postgresql+psycopg2://{envConfig.POSTGRES_USER}:{envConfig.POSTGRES_PASSWORD}@{envConfig.POSTGRES_HOST}:{envConfig.POSTGRES_PORT}/{envConfig.POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
