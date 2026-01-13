"""
LESSON 04: Persistent State & Cognitive Continuity
DESCRIPTION: Engineering a stateful session where the agent maintains context vectors across multiple turns.
ARCHITECT'S NOTE: Strategy is an iterative process. This build demonstrates 'Session Atomicity,' 
ensuring the agent retains critical business constraints (like the Innovation Budget) 
without requiring redundant prompt injection.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: The Continuity Specialist
    # We define the agent's ability to monitor and update its internal 'Context Blackboard.'
    context_lead = Agent(
        name="Cognitive_Strategy_Partner",
        instruction=(
            "You are a Senior Strategy Partner. Your primary function is 'Stateful Reasoning.' "
            "You must maintain an internal ledger of all variables, budgets, and constraints "
            "provided during this session. Use this shared history to inform all subsequent "
            "strategic recommendations."
        ),
        model=get_model()
    )

    runner = get_runner(context_lead)
    
    # 2. STATE PERSISTENCE: Initializing the Global Session Vector
    # We register a single session_id to be reused for the entire 'Strategy Workshop.'
    user_id, session_id = await initialize_session()
    
    print(f"--- [SYSTEM] Establishing Persistent Context | Session: {session_id} ---")

    # --- TURN 1: State Injection (The Budget Constraint) ---
    print("\n[INJECTING STATE] Registering 2026 AI Innovation Budget: $4.5M")
    turn_1_query = "Establish the 2026 AI Innovation Budget at $4.5 Million. Acknowledge and store this constraint."
    content_1 = types.Content(role="user", parts=[types.Part(text=turn_1_query)])
    
    events_1 = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_1)
    async for event in events_1:
        if event.is_final_response():
            print(f"Partner Response: {event.content.parts[0].text}")

    # --- TURN 2: State Retrieval (The Logic Test) ---
    # ARCHITECT'S NOTE: We intentionally omit the dollar amount to test state persistence.
    print("\n[RECOVERING STATE] Calculating project splits based on stored budget...")
    turn_2_query = "Based on that specific budget, propose a 40/30/30 split across three high-impact Pilot Projects. Detail the ROI for each."
    content_2 = types.Content(role="user", parts=[types.Part(text=turn_2_query)])
    
    events_2 = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_2)
    async for event in events_2:
        if event.is_final_response():
            print(f"\n--- [STRATEGIC ALLOCATION] ---\n{event.content.parts[0].text}")

    # 3. LIFECYCLE MANAGEMENT: Closing the stateful socket
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Session State Corruption: {e} ---")