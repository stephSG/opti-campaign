# This file contains all the Create, Read, Update, Delete (CRUD)
# operations for interacting with the database.
# This abstracts the database logic from the API endpoint logic.
# All code, comments, and docstrings are in English.

from sqlalchemy.orm import Session
# Use relative imports (.) for sibling modules
from . import models, schemas

# --- Campaign CRUD Operations ---

def get_campaign(db: Session, campaign_id: int) -> models.Campaign | None:
    """
    Fetches a single campaign from the database by its ID.

    Args:
        db (Session): The SQLAlchemy database session.
        campaign_id (int): The ID of the campaign to retrieve.

    Returns:
        models.Campaign | None: The campaign model instance or None if not found.
    """
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()

def get_campaigns(db: Session, skip: int = 0, limit: int = 100) -> list[models.Campaign]:
    """
    Fetches a list of campaigns from the database with pagination.

    Args:
        db (Session): The SQLAlchemy database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.

    Returns:
        list[models.Campaign]: A list of campaign model instances.
    """
    return db.query(models.Campaign).offset(skip).limit(limit).all()

def create_campaign(db: Session, campaign: schemas.CampaignCreate) -> models.Campaign:
    """
    Creates a new campaign record in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        campaign (schemas.CampaignCreate): The Pydantic schema with campaign data.

    Returns:
        models.Campaign: The newly created campaign model instance.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema
    db_campaign = models.Campaign(**campaign.model_dump())

    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign) # Refresh to get the new ID from the DB
    return db_campaign

def update_campaign(db: Session, campaign_id: int, campaign: schemas.CampaignUpdate) -> models.Campaign | None:
    """
    Updates an existing campaign in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        campaign_id (int): The ID of the campaign to update.
        campaign (schemas.CampaignUpdate): The Pydantic schema with updated data.

    Returns:
        models.Campaign | None: The updated campaign model instance or None if not found.
    """
    db_campaign = get_campaign(db, campaign_id=campaign_id)

    if db_campaign:
        # Get the update data from the Pydantic model
        # exclude_unset=True ensures we only update fields that were actually provided
        update_data = campaign.model_dump(exclude_unset=True)

        # Iterate over the provided data and update the SQLAlchemy model
        for key, value in update_data.items():
            setattr(db_campaign, key, value)

        db.commit()
        db.refresh(db_campaign)

    return db_campaign

def delete_campaign(db: Session, campaign_id: int) -> models.Campaign | None:
    """
    Deletes a campaign from the database.

    Args:
        db (Session): The SQLAlchemy database session.
        campaign_id (int): The ID of the campaign to delete.

    Returns:
        models.Campaign | None: The deleted campaign model instance or None if not found.
    """
    db_campaign = get_campaign(db, campaign_id=campaign_id)

    if db_campaign:
        db.delete(db_campaign)
        db.commit()

    return db_campaign

