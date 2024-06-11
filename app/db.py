from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(settings.MYSQL_URL.unicode_string())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

