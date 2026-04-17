from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ─── HCP Schemas ───
class HCPBase(BaseModel):
    name: str
    specialty: str = ""
    organization: str = ""
    email: str = ""
    phone: str = ""
    territory: str = ""


class HCPCreate(HCPBase):
    pass


class HCPResponse(HCPBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Interaction Schemas ───
class InteractionBase(BaseModel):
    hcp_id: int
    interaction_type: str = "Meeting"
    date: str = ""
    time: str = ""
    attendees: str = ""
    topics_discussed: str = ""
    notes: str = ""
    summary: str = ""
    sentiment: str = "Neutral"
    outcomes: str = ""
    materials_shared: str = ""
    samples_distributed: str = ""
    follow_up_actions: str = ""


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    hcp_id: Optional[int] = None
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    notes: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    follow_up_actions: Optional[str] = None


class InteractionResponse(InteractionBase):
    id: int
    hcp_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── FollowUp Schemas ───
class FollowUpBase(BaseModel):
    interaction_id: int
    date: str = ""
    follow_up_type: str = "Call"
    notes: str = ""
    status: str = "Pending"


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpResponse(FollowUpBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Chat Schemas ───
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []


class ExtractedFormData(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    follow_up_actions: Optional[str] = None
    notes: Optional[str] = None
    clear_form: Optional[bool] = None


class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    extracted_data: Optional[ExtractedFormData] = None
    interaction_id: Optional[int] = None
