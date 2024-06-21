from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from config.database import Base, engine

Base = declarative_base()
class Task(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
    create_on = Column(DateTime, default=datetime.utcnow)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
