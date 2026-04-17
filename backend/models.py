from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class InteractionType(str, enum.Enum):
    MEETING = "Meeting"
    CALL = "Call"
    EMAIL = "Email"
    VISIT = "Visit"
    CONFERENCE = "Conference"


class SentimentType(str, enum.Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class FollowUpStatus(str, enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    specialty = Column(String(255), default="")
    organization = Column(String(255), default="")
    email = Column(String(255), default="")
    phone = Column(String(50), default="")
    territory = Column(String(255), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interactions = relationship("Interaction", back_populates="hcp")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    interaction_type = Column(String(50), default="Meeting")
    date = Column(String(20), default="")
    time = Column(String(20), default="")
    attendees = Column(Text, default="")
    topics_discussed = Column(Text, default="")
    notes = Column(Text, default="")
    summary = Column(Text, default="")
    sentiment = Column(String(20), default="Neutral")
    outcomes = Column(Text, default="")
    materials_shared = Column(Text, default="")
    samples_distributed = Column(Text, default="")
    follow_up_actions = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    hcp = relationship("HCP", back_populates="interactions")
    follow_ups = relationship("FollowUp", back_populates="interaction")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    date = Column(String(20), default="")
    follow_up_type = Column(String(50), default="Call")
    notes = Column(Text, default="")
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("Interaction", back_populates="follow_ups")
