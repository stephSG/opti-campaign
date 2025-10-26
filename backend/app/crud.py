from sqlalchemy.orm import Session
from . import models, schemas
from .dependencies import get_password_hash # Import hashing function

# --- User CRUD ---

def get_user_by_username(db: Session, username: str):
    """
    Fetch a single user from the database by their username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.
    Hashes the password before storing.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Campaign CRUD ---

def get_campaign(db: Session, campaign_id: int):
    """
    Fetch a single campaign from the database by its ID.
    """
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetch a list of campaigns from the database with pagination.
    """
    return db.query(models.Campaign).offset(skip).limit(limit).all()

def create_campaign(db: Session, campaign: schemas.CampaignCreate):
    """
    Create a new campaign in the database.
    """
    db_campaign = models.Campaign(**campaign.model_dump())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def update_campaign(db: Session, db_campaign: models.Campaign, campaign_in: schemas.CampaignUpdate):
    """
    Update an existing campaign in the database.
    """
    # Get campaign data as a dict
    update_data = campaign_in.model_dump(exclude_unset=True)

    # Update model fields
    for key, value in update_data.items():
        setattr(db_campaign, key, value)

    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def delete_campaign(db: Session, db_campaign: models.Campaign):
    """
    Delete a campaign from the database.
    """
    db.delete(db_campaign)
    db.commit()
    return db_campaign
