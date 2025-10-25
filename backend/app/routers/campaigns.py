# This file defines the API endpoints for managing campaigns.
# All endpoints in this router are protected and require authentication.
# All code, comments, and docstrings are in English.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Use relative imports (..) to go up one level from 'routers' to 'app'
from .. import crud, models, schemas, dependencies, database

# Create the API router
router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
    # Apply the authentication dependency to all endpoints in this router
    dependencies=[Depends(dependencies.get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/",
             response_model=schemas.Campaign,
             status_code=status.HTTP_201_CREATED,
             summary="Create a new campaign")
def create_campaign(
        campaign: schemas.CampaignCreate,
        db: Session = Depends(database.get_db)
):
    """
    Create a new campaign.

    - **name**: The name of the campaign.
    - **budget**: The total budget allocated.
    - **status**: The current status (e.g., "active", "paused").
    """
    return crud.create_campaign(db=db, campaign=campaign)


@router.get("/",
            response_model=List[schemas.Campaign],
            summary="Get a list of all campaigns")
def read_campaigns(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db)
):
    """
    Retrieve a list of campaigns with pagination.
    """
    campaigns = crud.get_campaigns(db, skip=skip, limit=limit)
    return campaigns


@router.get("/{campaign_id}",
            response_model=schemas.Campaign,
            summary="Get a specific campaign by ID")
def read_campaign(
        campaign_id: int,
        db: Session = Depends(database.get_db)
):
    """
    Retrieve a single campaign by its unique ID.
    """
    db_campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign


@router.put("/{campaign_id}",
            response_model=schemas.Campaign,
            summary="Update an existing campaign")
def update_campaign(
        campaign_id: int,
        campaign: schemas.CampaignUpdate,
        db: Session = Depends(database.get_db)
):
    """
    Update a campaign's details.
    Only the provided fields will be updated.
    """
    db_campaign = crud.update_campaign(db, campaign_id=campaign_id, campaign=campaign)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign


@router.delete("/{campaign_id}",
               response_model=schemas.Campaign,
               summary="Delete a campaign")
def delete_campaign(
        campaign_id: int,
        db: Session = Depends(database.get_db)
):
    """
    Delete a campaign by its unique ID.
    """
    db_campaign = crud.delete_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

