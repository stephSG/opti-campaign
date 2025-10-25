from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL for SQLite.
# "sqlite:///./sql_app.db" means it will use a file named 'sql_app.db'
# in the same directory as the script that runs the app.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create the SQLAlchemy engine.
# connect_args={"check_same_thread": False} is needed only for SQLite
# to allow multiple threads to interact with the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of this class
# will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class. Our database models will inherit from this class.
Base = declarative_base()
