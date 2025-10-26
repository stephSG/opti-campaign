from sqlalchemy import Boolean, Column, Float, Integer, String, Date
from .database import Base

class User(Base):
    """
    User model for database storage.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Campaign(Base):
    """
    Campaign model for database storage.
    Represents an advertising campaign.
    """
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    status = Column(Boolean, default=True) # True=Active, False=Inactive
