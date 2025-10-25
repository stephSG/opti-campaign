from pydantic import BaseModel
from typing import Optional
import datetime

# ------------------------------
# Schemas for Campaigns
# ------------------------------

class CampaignBase(BaseModel):
    """
    Base schema for a Campaign. Contains all common fields
    that are shared across creation, update, and read.
    """
    name: str
    description: Optional[str] = None
    start_date: datetime.date
    end_date: datetime.date
    budget: float
    status: bool = True

class CampaignCreate(CampaignBase):
    """
    Schema used for creating a new campaign.
    It inherits all fields from CampaignBase.
    """
    pass

class CampaignUpdate(BaseModel):
    """
    Schema used for updating an existing campaign.
    All fields are optional, so only provided fields are updated.
    This does NOT inherit from CampaignBase to allow partial updates.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    budget: Optional[float] = None
    status: Optional[bool] = None

class Campaign(CampaignBase):
    """
    Schema used for reading/returning campaign data from the API.
    It includes the 'id' and enables ORM mode to map from the
    SQLAlchemy model to the Pydantic model.
    """
    id: int

    class Config:
        # Pydantic's orm_mode will tell Pydantic to read the data
        # even if it is not a dict, but an ORM model (like our Campaign model).
        orm_mode = True

# ------------------------------
# Schemas for Authentication
# ------------------------------

class Token(BaseModel):
    """
    Schema for the JWT access token response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data contained within the JWT token (the 'sub' claim).
    """
    username: Optional[str] = None

class User(BaseModel):
    """
    Base user schema (for internal representation, e.g., in auth dependencies).
    """
    username: str

class UserInDB(User):
    """
    Schema for a user object as stored in the database (includes hashed password).
    We don't create a real user model for this simple app, but this
    schema is used by the auth logic (e.g., in crud.py) to represent
    a user retrieved from a (mock) database.
    """
    hashed_password: str
