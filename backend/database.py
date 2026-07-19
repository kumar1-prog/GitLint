from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create_engine = opens the connection to PostgreSQL
# It doesn't actually connect yet — it just prepares the connection pool
# A connection pool = multiple connections ready to use
# so requests don't wait for each other
# If DATABASE_URL is wrong → this line throws an error immediately
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates database sessions
# A session = one unit of work with the DB
# Think of it like a transaction — you open it, do stuff, close it
# autocommit=False means changes aren't saved until you explicitly call commit()
# autoflush=False means SQLAlchemy won't auto-send pending changes to DB
# before every query — we control when that happens
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our DB models will inherit from
# SQLAlchemy uses it to track which classes = which tables
Base = declarative_base()


# This is a dependency function — FastAPI calls it automatically
# for every route that needs DB access
# It opens a session, yields it to the route, then closes it
# The try/finally guarantees the session closes even if the route crashes
# If we don't close sessions → connection pool exhausts → app hangs
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# This reads all classes that inherit from Base
# and creates their corresponding tables in PostgreSQL
# If table already exists → skips it (doesn't overwrite)
# If table is new → creates it
# Call this once when app starts
def create_tables():
    Base.metadata.create_all(bind=engine)