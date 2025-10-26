from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# --- Campaign Schemas ---

class CampaignBase(BaseModel):
    """
    Base schema for a campaign, containing all common fields.
    """
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    budget: float
    status: bool = True

class CampaignCreate(CampaignBase):
    """
    Schema for creating a new campaign. Inherits from CampaignBase.
    """
    pass

class CampaignUpdate(CampaignBase):
    """
    Schema for updating an existing campaign.
    All fields are optional.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    status: Optional[bool] = None

class Campaign(CampaignBase):
    """
    Schema for reading a campaign from the API (e.g., in a response).
    Includes the 'id' field and enables ORM mode.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

class UserBase(BaseModel):
    """
    Base schema for a user, containing the username.
    """
    username: str

class UserCreate(UserBase):
    """
    Schema for creating a new user. Includes the password.
    """
    password: str

class User(UserBase):
    """
    Schema for reading a user from the API.
    Excludes sensitive information like the password.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Token Schemas ---

class Token(BaseModel):
    """
    Schema for the JWT access token response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data contained within the JWT token.
    """
    username: Optional[str] = None
