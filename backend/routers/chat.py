from fastapi import APIRouter
from schemas import ChatRequest, ChatResponse
from agent import run_agent

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message through the LangGraph AI agent."""
    history = [{"role": m.role, "content": m.content} for m in request.conversation_history]

    result = run_agent(
        message=request.message,
        conversation_history=history,
    )

    return ChatResponse(
        response=result["response"],
        tool_used=result.get("tool_used"),
        extracted_data=result.get("extracted_data"),
        interaction_id=result.get("interaction_id"),
    )
