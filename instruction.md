# Technical Challenge

## Overview
Build a split-screen application with:

### Left Panel: Interaction Form
Contains structured fields:
- HCP Name
- Date
- Sentiment
- Materials Shared (e.g., brochures)

### Right Panel: AI Assistant Chat
- User interacts using natural language
- AI updates the form automatically

---

## Core Rule
You must NOT manually edit the form.

All updates must be done via:
- AI Assistant  
- LangGraph Tools  
- LLM (Large Language Model)

---

## Required Tools (LangGraph)

You must implement at least 5 tools.

---

### 1. Log Interaction Tool (Mandatory)

**Purpose:** Extract structured data and fill the form.

**Example Input:**
> Today I met with Dr. Smith and discussed product X efficiency. The sentiment was positive and I shared the brochures.

**Expected Output:**
- HCP Name → Dr. Smith  
- Date → Today  
- Sentiment → Positive  
- Brochures Shared → Yes  

---

### 2. Edit Interaction Tool (Mandatory)

**Purpose:** Update only specific fields.

**Example Input:**
> Sorry, the name was actually Dr. John and the sentiment was negative.

**Expected Output:**
- HCP Name → Dr. John  
- Sentiment → Negative  
- Other fields remain unchanged  

---

## Additional Tools (Choose Any 3)

### 3. Clear Form Tool
- Reset all fields to default or empty

### 4. Summarize Interaction Tool
- Generate a summary from form data

### 5. Validate Form Tool
- Check required fields
- Return missing fields if any

---

## Technical Requirements

- Must use:
  - LangGraph
  - LLM (e.g., OpenAI)

- No hardcoded logic  
- Tool execution must be LLM-driven  

---

## Goal

- User chats with AI (right panel)
- AI uses LangGraph tools
- Tools update the form (left panel)

Build an AI-driven interaction logging system.

---

## Success Criteria

- Split UI implemented  
- AI correctly fills and updates the form  
- Minimum 5 tools implemented  
- Uses LangGraph and LLM properly  
- No manual form interaction  

---

## Optional Enhancements

- Add tool execution logs  
- Show reasoning steps  
- Improve UI/UX  

---