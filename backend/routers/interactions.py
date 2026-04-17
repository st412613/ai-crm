from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import crud
from schemas import (
    InteractionCreate, InteractionUpdate, InteractionResponse,
    HCPResponse, HCPCreate, FollowUpCreate, FollowUpResponse
)

router = APIRouter(prefix="/api", tags=["interactions"])


# ─── HCP Endpoints ───
@router.get("/hcps", response_model=List[HCPResponse])
def list_hcps(search: str = "", db: Session = Depends(get_db)):
    hcps = crud.get_hcps(db, search=search)
    return hcps


@router.post("/hcps", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    return crud.create_hcp(db, hcp)


@router.get("/hcps/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = crud.get_hcp(db, hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp


# ─── Interaction Endpoints ───
@router.get("/interactions", response_model=List[InteractionResponse])
def list_interactions(
    hcp_id: Optional[int] = None,
    search: str = "",
    db: Session = Depends(get_db)
):
    interactions = crud.get_interactions(db, hcp_id=hcp_id, search=search)
    result = []
    for i in interactions:
        data = InteractionResponse.model_validate(i)
        hcp = crud.get_hcp(db, i.hcp_id)
        data.hcp_name = hcp.name if hcp else "Unknown"
        result.append(data)
    return result


@router.post("/interactions", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    hcp = crud.get_hcp(db, interaction.hcp_id)
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    created = crud.create_interaction(db, interaction)
    data = InteractionResponse.model_validate(created)
    data.hcp_name = hcp.name
    return data


@router.get("/interactions/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = crud.get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    data = InteractionResponse.model_validate(interaction)
    hcp = crud.get_hcp(db, interaction.hcp_id)
    data.hcp_name = hcp.name if hcp else "Unknown"
    return data


@router.put("/interactions/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction: InteractionUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_interaction(db, interaction_id, interaction)
    if not updated:
        raise HTTPException(status_code=404, detail="Interaction not found")
    data = InteractionResponse.model_validate(updated)
    hcp = crud.get_hcp(db, updated.hcp_id)
    data.hcp_name = hcp.name if hcp else "Unknown"
    return data


@router.delete("/interactions/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    success = crud.delete_interaction(db, interaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"message": "Interaction deleted successfully"}


# ─── FollowUp Endpoints ───
@router.get("/follow-ups", response_model=List[FollowUpResponse])
def list_follow_ups(
    interaction_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_follow_ups(db, interaction_id=interaction_id)


@router.post("/follow-ups", response_model=FollowUpResponse)
def create_follow_up(follow_up: FollowUpCreate, db: Session = Depends(get_db)):
    return crud.create_follow_up(db, follow_up)
