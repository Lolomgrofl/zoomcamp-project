from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
