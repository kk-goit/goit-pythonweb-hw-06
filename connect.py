from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

url_to_db = "postgresql+psycopg2://postgres:qwerty@localhost:5432/hw06"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()