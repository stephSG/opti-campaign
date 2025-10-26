from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/campaigns",
    tags=["campaigns"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(
        campaign: schemas.CampaignCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new campaign.
    """
    return crud.create_campaign(db=db, campaign=campaign)

@router.get("/", response_model=List[schemas.Campaign])
def read_campaigns(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Retrieve a list of campaigns with pagination.
    """
    campaigns = crud.get_campaigns(db, skip=skip, limit=limit)
    return campaigns

@router.get("/{campaign_id}", response_model=schemas.Campaign)
def read_campaign(
        campaign_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieve a single campaign by its ID.
    """
    db_campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.put("/{campaign_id}", response_model=schemas.Campaign)
def update_campaign(
        campaign_id: int,
        campaign_in: schemas.CampaignUpdate,
        db: Session = Depends(get_db)
):
    """
    Update an existing campaign by its ID.
    """
    db_campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return crud.update_campaign(db=db, db_campaign=db_campaign, campaign_in=campaign_in)

@router.delete("/{campaign_id}", response_model=schemas.Campaign)
def delete_campaign(
        campaign_id: int,
        db: Session = Depends(get_db)
):
    """
    Delete a campaign by its ID.
    """
    db_campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return crud.delete_campaign(db=db, db_campaign=db_campaign)

@router.patch("/{campaign_id}/toggle", response_model=schemas.Campaign)
def toggle_campaign_status(
        campaign_id: int,
        db: Session = Depends(get_db)
):
    """
    Toggle the status (active/inactive) of a campaign.
    """
    db_campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Toggle the status
    new_status = not db_campaign.status
    campaign_update = schemas.CampaignUpdate(status=new_status)

    return crud.update_campaign(db=db, db_campaign=db_campaign, campaign_in=campaign_update)
