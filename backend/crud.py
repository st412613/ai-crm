from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import HCP, Interaction, FollowUp
from schemas import InteractionCreate, InteractionUpdate, HCPCreate, FollowUpCreate
from typing import Optional, List


# ─── HCP CRUD ───
def get_hcps(db: Session, search: str = "", limit: int = 100):
    query = db.query(HCP)
    if search:
        query = query.filter(HCP.name.ilike(f"%{search}%"))
    return query.order_by(HCP.name).limit(limit).all()


def get_hcp(db: Session, hcp_id: int):
    return db.query(HCP).filter(HCP.id == hcp_id).first()


def get_hcp_by_name(db: Session, name: str):
    return db.query(HCP).filter(HCP.name.ilike(f"%{name}%")).first()


def create_hcp(db: Session, hcp: HCPCreate):
    db_hcp = HCP(**hcp.model_dump())
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp


# ─── Interaction CRUD ───
def get_interactions(db: Session, hcp_id: Optional[int] = None, search: str = "", limit: int = 50):
    query = db.query(Interaction)
    if hcp_id:
        query = query.filter(Interaction.hcp_id == hcp_id)
    if search:
        query = query.filter(
            or_(
                Interaction.topics_discussed.ilike(f"%{search}%"),
                Interaction.notes.ilike(f"%{search}%"),
                Interaction.summary.ilike(f"%{search}%"),
                Interaction.outcomes.ilike(f"%{search}%"),
            )
        )
    return query.order_by(Interaction.created_at.desc()).limit(limit).all()


def get_interaction(db: Session, interaction_id: int):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def create_interaction(db: Session, interaction: InteractionCreate):
    db_interaction = Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def update_interaction(db: Session, interaction_id: int, interaction: InteractionUpdate):
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        return None
    update_data = interaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_interaction, key, value)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def delete_interaction(db: Session, interaction_id: int):
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if db_interaction:
        db.delete(db_interaction)
        db.commit()
        return True
    return False


# ─── FollowUp CRUD ───
def get_follow_ups(db: Session, interaction_id: Optional[int] = None, limit: int = 50):
    query = db.query(FollowUp)
    if interaction_id:
        query = query.filter(FollowUp.interaction_id == interaction_id)
    return query.order_by(FollowUp.created_at.desc()).limit(limit).all()


def create_follow_up(db: Session, follow_up: FollowUpCreate):
    db_follow_up = FollowUp(**follow_up.model_dump())
    db.add(db_follow_up)
    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up


def update_follow_up_status(db: Session, follow_up_id: int, status: str):
    db_follow_up = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
    if db_follow_up:
        db_follow_up.status = status
        db.commit()
        db.refresh(db_follow_up)
    return db_follow_up
