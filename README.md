# AI-First CRM – HCP Module (LogInteractionScreen)

An AI-powered CRM system for managing Healthcare Professional (HCP) interactions, built with a **LangGraph AI agent** that uses **Groq LLMs** for intelligent interaction logging.

## 🏗️ Architecture

```
┌──────────────────────┐     ┌──────────────────────┐
│   React + Redux      │────▶│  FastAPI Backend      │
│   (Vite)             │◀────│                       │
│                      │     │  ┌─── LangGraph ───┐  │
│  ┌─────────┬───────┐ │     │  │  AI Agent       │  │
│  │  Form   │ Chat  │ │     │  │  (5 Tools)      │  │
│  │  Panel  │ Panel │ │     │  │                 │  │
│  └─────────┴───────┘ │     │  └───────┬─────────┘  │
│                      │     │          │             │
│  ┌─────────────────┐ │     │  ┌───────▼─────────┐  │
│  │ Interaction List│ │     │  │  Groq LLM       │  │
│  └─────────────────┘ │     │  │  (gemma2-9b-it) │  │
└──────────────────────┘     │  └─────────────────┘  │
                             │          │             │
                             │  ┌───────▼─────────┐  │
                             │  │  SQLite DB      │  │
                             │  └─────────────────┘  │
                             └──────────────────────┘
```

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Redux Toolkit |
| Backend | Python + FastAPI |
| AI Agent | LangGraph |
| LLM | Groq (gemma2-9b-it) |
| Database | SQLite (SQLAlchemy ORM) |
| Font | Google Inter |

## 🤖 LangGraph Agent – 5 Tools

1. **Log Interaction** – Extracts HCP name, sentiment, topics, materials from natural language and saves to DB
2. **Edit Interaction** – Modifies existing interaction fields by ID
3. **Search HCP History** – Queries past interactions with keyword/date filtering
4. **Schedule Follow-up** – Creates follow-up tasks (calls, meetings) from natural language
5. **Generate Interaction Report** – Produces summary report with sentiment trends for an HCP

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key ([get one here](https://console.groq.com))

### Backend
```bash
cd backend
pip install -r requirements.txt
# Set your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
# Seed sample data
python3 seed.py
# Start server
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

## 📱 Features

- **Dual-mode logging**: Structured form OR conversational AI chat
- **AI auto-fill**: Chat with the AI and form fields populate automatically
- **Entity extraction**: LLM extracts HCP names, sentiment, topics, dates from free text
- **Interaction history**: Browse and search past interactions
- **Follow-up scheduling**: Schedule calls/meetings via natural language
- **Reporting**: Generate HCP engagement summaries

## 📂 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # DB models (HCP, Interaction, FollowUp)
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── agent.py             # LangGraph agent + 5 tools
│   ├── seed.py              # Sample data seeder
│   ├── routers/
│   │   ├── interactions.py  # REST API endpoints
│   │   └── chat.py          # Chat/AI endpoint
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api.js           # Backend API client
│   │   ├── store/           # Redux store + slices
│   │   ├── components/      # React components
│   │   └── index.css        # Global styles
│   └── package.json
│
└── README.md
```
