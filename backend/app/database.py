from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL for SQLite.
# The database file will be named 'opti-campaign.db' in the root directory.
DATABASE_URL = "sqlite:///./opti-campaign.db"

# Create the SQLAlchemy engine.
# connect_args is needed only for SQLite to allow multithreading.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. This will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class.
# Our ORM models will inherit from this class.
Base = declarative_base()
