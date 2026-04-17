"""
LangGraph AI Agent for HCP CRM
5 Tools: log_interaction, edit_interaction, search_hcp_history, schedule_follow_up, generate_report
Uses Groq gemma2-9b-it via LangChain
"""
import os
import json
from datetime import datetime, timedelta
from typing import Annotated, TypedDict, Literal, Optional
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import InteractionCreate, InteractionUpdate, FollowUpCreate, HCPCreate

load_dotenv()

# ─── LLM Setup ───
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)


# ─── Tool Definitions ───
@tool
def log_interaction(
    hcp_name: str,
    interaction_type: str = "Meeting",
    date: str = "",
    time: str = "",
    attendees: str = "",
    topics_discussed: str = "",
    sentiment: str = "Neutral",
    outcomes: str = "",
    materials_shared: str = "",
    samples_distributed: str = "",
    follow_up_actions: str = "",
    notes: str = "",
) -> str:
    """Log a new HCP interaction. Use this when the user describes a meeting, call, visit, or other interaction with a healthcare professional.
    Extract all relevant fields from the user's description. THIS TOOL DOES NOT SAVE TO DB, it just extracts the fields for the UI form.
    
    Args:
        hcp_name: Name of the Healthcare Professional (e.g., "Dr. Smith")
        interaction_type: Type of interaction - Meeting, Call, Email, Visit, or Conference
        date: Date of interaction (e.g., "2025-04-15" or "today")
        time: Time of interaction (e.g., "07:36 PM")
        attendees: People who attended (comma-separated)
        topics_discussed: Key discussion topics
        sentiment: Observed HCP sentiment - Positive, Neutral, or Negative
        outcomes: Key outcomes or agreements from the interaction
        materials_shared: Materials shared (e.g., "Brochures, Product info")
        samples_distributed: Samples distributed (e.g., "Product X samples")
        follow_up_actions: Planned follow-up actions
        notes: Additional notes about the interaction
    """
    try:
        # Default date to today if not specified
        if not date or date.lower() == "today":
            date = datetime.now().strftime("%Y-%m-%d")
        if not time:
            time = datetime.now().strftime("%I:%M %p")

        result = {
            "status": "success",
            "interaction_id": 0, # Transient ID
            "hcp_name": hcp_name,
            "interaction_type": interaction_type,
            "date": date,
            "time": time,
            "attendees": attendees,
            "topics_discussed": topics_discussed,
            "sentiment": sentiment,
            "outcomes": outcomes,
            "materials_shared": materials_shared,
            "samples_distributed": samples_distributed,
            "follow_up_actions": follow_up_actions,
            "notes": notes,
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
def edit_interaction(
    hcp_name: Optional[str] = None,
    interaction_id: Optional[int] = None,
    interaction_type: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    sentiment: Optional[str] = None,
    outcomes: Optional[str] = None,
    materials_shared: Optional[str] = None,
    samples_distributed: Optional[str] = None,
    follow_up_actions: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """Edit an existing HCP interaction that has ALREADY BEEN LOGGED and Saved. Use this when the user wants to modify or update a previously logged interaction.
    Only provide the fields that need to be changed. If interaction_id is not known, provide hcp_name.
    
    Args:
        hcp_name: Name of the HCP to edit the latest interaction for
        interaction_id: ID of the interaction to edit
        interaction_type: Updated interaction type
        date: Updated date
        time: Updated time
        attendees: Updated attendees
        topics_discussed: Updated topics
        sentiment: Updated sentiment
        outcomes: Updated outcomes
        materials_shared: Updated materials shared
        samples_distributed: Updated samples distributed
        follow_up_actions: Updated follow-up actions
        notes: Updated notes
    """
    db = SessionLocal()
    try:
        if not interaction_id and hcp_name:
            hcp = crud.get_hcp_by_name(db, hcp_name)
            if hcp:
                interactions = crud.get_interactions(db, hcp_id=hcp.id, limit=1)
                if interactions:
                    interaction_id = interactions[0].id

        if not interaction_id:
            return json.dumps({"status": "error", "message": "Could not determine which interaction to edit. No interaction ID or HCP Name provided."})

        update_data = {}
        if interaction_type is not None:
            update_data["interaction_type"] = interaction_type
        if date is not None:
            update_data["date"] = date
        if time is not None:
            update_data["time"] = time
        if attendees is not None:
            update_data["attendees"] = attendees
        if topics_discussed is not None:
            update_data["topics_discussed"] = topics_discussed
        if sentiment is not None:
            update_data["sentiment"] = sentiment
        if outcomes is not None:
            update_data["outcomes"] = outcomes
        if materials_shared is not None:
            update_data["materials_shared"] = materials_shared
        if samples_distributed is not None:
            update_data["samples_distributed"] = samples_distributed
        if follow_up_actions is not None:
            update_data["follow_up_actions"] = follow_up_actions
        if notes is not None:
            update_data["notes"] = notes

        interaction = crud.update_interaction(
            db, interaction_id, InteractionUpdate(**update_data)
        )
        if not interaction:
            return json.dumps({"status": "error", "message": f"Interaction {interaction_id} not found"})

        hcp = crud.get_hcp(db, interaction.hcp_id)
        return json.dumps({
            "status": "success",
            "interaction_id": interaction_id,
            "hcp_name": hcp.name if hcp else "Unknown",
            "updated_fields": list(update_data.keys()),
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()


@tool
def search_hcp_history(
    hcp_name: str,
    search_query: str = "",
    limit: int = 10,
) -> str:
    """Search interaction history for a specific HCP. Use this when the user wants to find past interactions, check history, or look up previous conversations with an HCP.
    
    Args:
        hcp_name: Name of the HCP to search for
        search_query: Optional keyword to filter interactions by topic, notes, or outcomes
        limit: Maximum number of results to return
    """
    db = SessionLocal()
    try:
        hcp = crud.get_hcp_by_name(db, hcp_name)
        if not hcp:
            return json.dumps({
                "status": "not_found",
                "message": f"No HCP found matching '{hcp_name}'"
            })

        interactions = crud.get_interactions(db, hcp_id=hcp.id, search=search_query, limit=limit)

        results = []
        for i in interactions:
            results.append({
                "id": i.id,
                "type": i.interaction_type,
                "date": i.date,
                "time": i.time,
                "topics": i.topics_discussed,
                "sentiment": i.sentiment,
                "outcomes": i.outcomes,
                "summary": i.summary or i.notes,
            })

        return json.dumps({
            "status": "success",
            "hcp_name": hcp.name,
            "hcp_id": hcp.id,
            "total_interactions": len(results),
            "interactions": results,
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()


@tool
def schedule_follow_up(
    follow_up_date: str,
    hcp_name: Optional[str] = None,
    interaction_id: Optional[int] = None,
    follow_up_type: str = "Call",
    notes: str = "",
) -> str:
    """Schedule a follow-up action for an HCP. Use this when the user wants to plan a future action like a call, meeting, or email.
    
    Args:
        follow_up_date: Date for the follow-up (e.g., "2025-04-20" or "next Tuesday")
        hcp_name: Name of the HCP to schedule follow up with
        interaction_id: Optional ID of the interaction this follow-up relates to
        follow_up_type: Type of follow-up - Call, Meeting, Email, or Visit
        notes: Notes about what the follow-up should cover
    """
    db = SessionLocal()
    try:
        if not interaction_id and hcp_name:
            hcp = crud.get_hcp_by_name(db, hcp_name)
            if hcp:
                interactions = crud.get_interactions(db, hcp_id=hcp.id, limit=1)
                if interactions:
                    interaction_id = interactions[0].id

        if not interaction_id:
            return json.dumps({"status": "error", "message": "Interaction ID could not be determined."})

        interaction = crud.get_interaction(db, interaction_id)
        if not interaction:
            return json.dumps({"status": "error", "message": f"Interaction {interaction_id} not found"})

        # Parse relative dates
        if "tomorrow" in follow_up_date.lower():
            follow_up_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "next week" in follow_up_date.lower():
            follow_up_date = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        elif "next" in follow_up_date.lower():
            # Simple attempt for "next Tuesday" etc
            follow_up_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        follow_up = crud.create_follow_up(db, FollowUpCreate(
            interaction_id=interaction_id,
            date=follow_up_date,
            follow_up_type=follow_up_type,
            notes=notes,
        ))

        hcp = crud.get_hcp(db, interaction.hcp_id)
        return json.dumps({
            "status": "success",
            "follow_up_id": follow_up.id,
            "interaction_id": interaction_id,
            "hcp_name": hcp.name if hcp else "Unknown",
            "date": follow_up_date,
            "type": follow_up_type,
            "notes": notes,
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()


@tool
def generate_interaction_report(
    hcp_name: str,
    limit: int = 10,
) -> str:
    """Generate a summary report of recent interactions with an HCP. Use this when the user wants an overview, analysis, or summary of their engagement with a particular HCP.
    
    Args:
        hcp_name: Name of the HCP to generate report for
        limit: Number of recent interactions to include
    """
    db = SessionLocal()
    try:
        hcp = crud.get_hcp_by_name(db, hcp_name)
        if not hcp:
            return json.dumps({
                "status": "not_found",
                "message": f"No HCP found matching '{hcp_name}'"
            })

        interactions = crud.get_interactions(db, hcp_id=hcp.id, limit=limit)

        if not interactions:
            return json.dumps({
                "status": "no_data",
                "hcp_name": hcp.name,
                "message": "No interactions found for this HCP"
            })

        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        interaction_types = {}
        all_topics = []
        all_outcomes = []
        all_materials = []

        for i in interactions:
            sentiment_counts[i.sentiment] = sentiment_counts.get(i.sentiment, 0) + 1
            interaction_types[i.interaction_type] = interaction_types.get(i.interaction_type, 0) + 1
            if i.topics_discussed:
                all_topics.append(i.topics_discussed)
            if i.outcomes:
                all_outcomes.append(i.outcomes)
            if i.materials_shared:
                all_materials.append(i.materials_shared)

        # Get follow-ups
        follow_ups = []
        for i in interactions:
            fups = crud.get_follow_ups(db, interaction_id=i.id)
            for f in fups:
                follow_ups.append({
                    "date": f.date,
                    "type": f.follow_up_type,
                    "status": f.status,
                    "notes": f.notes,
                })

        report = {
            "status": "success",
            "hcp_name": hcp.name,
            "hcp_specialty": hcp.specialty,
            "hcp_organization": hcp.organization,
            "total_interactions": len(interactions),
            "sentiment_distribution": sentiment_counts,
            "interaction_types": interaction_types,
            "recent_topics": all_topics[:5],
            "recent_outcomes": all_outcomes[:5],
            "materials_shared": all_materials[:5],
            "pending_follow_ups": [f for f in follow_ups if f["status"] == "Pending"],
            "date_range": {
                "earliest": interactions[-1].date if interactions else "",
                "latest": interactions[0].date if interactions else "",
            },
        }
        return json.dumps(report)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()


        db.close()


@tool
def clear_form() -> str:
    """Clear all form fields. Use this when the user asks to reset the form, clear the fields, cancel logging, or start over.
    This will wipe all current form data from the UI.
    """
    return json.dumps({"status": "success", "clear_form": True})


# ─── LangGraph Agent Setup ───
tools = [log_interaction, edit_interaction, search_hcp_history, schedule_follow_up, generate_interaction_report, clear_form]
llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


SYSTEM_PROMPT = """You are an AI assistant for a pharmaceutical CRM system, helping field representatives log and manage their interactions with Healthcare Professionals (HCPs).

You have 6 tools available:

1. **log_interaction** - Log a new interaction. Extract ALL relevant fields from the user's message:
   - hcp_name (required), interaction_type, date, time, attendees, topics_discussed, sentiment, outcomes, materials_shared, samples_distributed, follow_up_actions, notes
   
2. **edit_interaction** - Edit an existing interaction that has ALREADY BEEN SAVED TO THE DATABASE. Only update the fields the user wants to change.

3. **search_hcp_history** - Search past interactions for a specific HCP.

4. **schedule_follow_up** - Schedule follow-up actions (calls, meetings, emails) for an interaction.

5. **generate_interaction_report** - Generate a summary report of interactions with an HCP.

6. **clear_form** - Clear all fields in the currently active log form. Use this whenever the user requests to reset, clear, or cancel what they are currently logging.

Guidelines:
- When a user specifies logging a new interaction, or when they provide corrections to an interaction they are currently logging (e.g. "actually the name is John"), you MUST call the log_interaction tool AGAIN with all the combined/corrected fields. Do NOT use edit_interaction for corrections made while filling out the form.
- You MUST reply with exactly this formatted text to the user:
**Expected Output:**
- HCP Name → [HCP Name]
- Date → [Date]
- Sentiment → [Sentiment]
- Brochures Shared → [Yes if "brochures" mentioned, otherwise No]

- Extract as much information as possible from the user's message for the tool call (HCP name, sentiment, topics, materials, etc.)
- If the date isn't mentioned, default to today.
- If sentiment isn't explicitly stated, infer it from the context (words like "great", "interested" = Positive; "concerned", "hesitant" = Negative).
- Be concise but helpful in your responses.
- When the user asks about history or past interactions, use search_hcp_history.
- When the user asks for a summary or report, use generate_interaction_report.
"""


def agent_node(state: AgentState):
    messages = state["messages"]
    # Ensure system prompt is first
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "__end__"


# Build the graph
tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)
graph_builder.set_entry_point("agent")
graph_builder.add_conditional_edges("agent", should_continue, {"tools": "tools", "__end__": END})
graph_builder.add_edge("tools", "agent")

agent_graph = graph_builder.compile()


def run_agent(message: str, conversation_history: list = None) -> dict:
    """Run the LangGraph agent with a user message and return the response."""
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add conversation history
    if conversation_history:
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=message))

    result = agent_graph.invoke({"messages": messages})

    # Extract the final response and any tool results
    last_ai_message = None
    tool_used = None
    tool_result = None

    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content and not getattr(msg, "tool_calls", None):
            last_ai_message = msg.content
            break

    # Find tool calls and results
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_used = msg.tool_calls[0]["name"]
        if isinstance(msg, ToolMessage):
            try:
                tool_result = json.loads(msg.content)
            except json.JSONDecodeError:
                tool_result = {"raw": msg.content}

    # Build extracted form data from tool results
    extracted_data = None
    interaction_id = None

    if tool_result and isinstance(tool_result, dict):
        if tool_result.get("status") == "success":
            interaction_id = tool_result.get("interaction_id")
            if tool_used == "log_interaction":
                extracted_data = {
                    "hcp_name": tool_result.get("hcp_name"),
                    "interaction_type": tool_result.get("interaction_type"),
                    "date": tool_result.get("date"),
                    "time": tool_result.get("time"),
                    "attendees": tool_result.get("attendees"),
                    "topics_discussed": tool_result.get("topics_discussed"),
                    "sentiment": tool_result.get("sentiment"),
                    "outcomes": tool_result.get("outcomes"),
                    "materials_shared": tool_result.get("materials_shared"),
                    "samples_distributed": tool_result.get("samples_distributed"),
                    "follow_up_actions": tool_result.get("follow_up_actions"),
                    "notes": tool_result.get("notes"),
                }
            elif tool_used == "clear_form":
                extracted_data = {"clear_form": True}

    return {
        "response": last_ai_message or "I've processed your request.",
        "tool_used": tool_used,
        "extracted_data": extracted_data,
        "interaction_id": interaction_id,
    }
