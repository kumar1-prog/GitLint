from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from database import Base


# Each class = one table in PostgreSQL
# Each class attribute = one column in that table
# SQLAlchemy reads these classes and creates the actual tables

class User(Base):
    # __tablename__ tells SQLAlchemy what to name the table in PostgreSQL
    __tablename__ = "users"

    # Integer primary key that auto-increments
    # Every user gets a unique ID automatically
    id = Column(Integer, primary_key=True, index=True)

    # index=True creates a DB index on this column
    # Index = like a book index — makes lookups by github_username fast
    # Without index, DB scans every row to find a username — slow at scale
    github_username = Column(String, unique=True, index=True)
    # unique=True means two users can't have same username
    # If you try to insert a duplicate → DB throws IntegrityError

    avatar_url = Column(String, nullable=True)
    # nullable=True means this column can be empty
    # nullable=False (default) means it MUST have a value

    # func.now() = PostgreSQL fills this automatically with current timestamp
    # We never set this manually — DB handles it
    created_at = Column(DateTime, server_default=func.now())


class AuditReport(Base):
    __tablename__ = "audit_reports"

    id = Column(Integer, primary_key=True, index=True)

    github_username = Column(String, index=True)
    # index=True here because we'll frequently query
    # "give me all audits for username X"

    overall_score = Column(Integer)

    # Individual signal scores stored as separate columns
    # We could store the whole report as one JSON blob
    # but separate columns let us run SQL queries like:
    # "SELECT AVG(readme_score) FROM audit_reports"
    # which is how we calculate peer benchmarks
    consistency_score = Column(Integer)
    fork_ratio_score = Column(Integer)
    readme_score = Column(Integer)
    diversity_score = Column(Integer)
    depth_score = Column(Integer)
    benchmark_score = Column(Integer)

    # Full report stored as JSON too — for the frontend to display
    # JSON column in PostgreSQL stores the dict as-is
    full_report = Column(JSON)

    # server_default vs default:
    # server_default = DB sets the value (faster, no Python involved)
    # default = SQLAlchemy sets the value in Python before inserting
    created_at = Column(DateTime, server_default=func.now())

    