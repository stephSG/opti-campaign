from sqlalchemy import Boolean, Column, Integer, String, Float, Date
from .database import Base  # Import the Base from our database.py file

class Campaign(Base):
    """
    SQLAlchemy model representing a marketing campaign.
    """
    __tablename__ = "campaigns"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Campaign Details
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Financials
    budget = Column(Float, nullable=False)

    # Status (e.g., Active/Inactive)
    # Defaults to True, meaning the campaign is active by default.
    status = Column(Boolean, default=True)
