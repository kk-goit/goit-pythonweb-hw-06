from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf.vars import VARS

engine = create_engine(VARS["DB_URI"])
SessionLocal = sessionmaker(bind=engine)
