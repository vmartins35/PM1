import enum
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base, Session


class Config:

    @staticmethod
    def get_database_url():
       return f'sqlite:///{Config.get_project_root()}/database.db'

    @staticmethod
    def get_project_root():
        return Path(__file__).parent.parent


engine = create_engine(Config.get_database_url(), echo=False,
                       connect_args={'check_same_thread': False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
