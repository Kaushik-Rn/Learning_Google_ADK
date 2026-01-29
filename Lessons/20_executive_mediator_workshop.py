"""
LESSON 20: Collaborative Multi-User Sessions & Conflict Mediation
DESCRIPTION: Managing distinct stakeholder perspectives within a single thread.
ARCHITECT'S NOTE: Strategy is the art of compromise. By tagging inputs with 
Stakeholder Roles and maintaining a unified session state, we enable the 
agent to perform 'Conflict Mapping'—identifying the exact delta between 
departmental mandates and proposing a reconciled executive summary.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def record_executive_input(runner, session_id, admin_id, role, statement):
    """
    Injects departmental input into the session history using a unified owner.
    """
    print(f"--- [INPUT CAPTURED] Role: {role:>10} ---")
    
    # We use explicit tagging to ensure the LLM knows WHO said WHAT
    stakeholder_context = f"OFFICIAL STAKEHOLDER INPUT | ROLE: {role} | MANDATE: {statement}"
    content = types.Content(role="user", parts=[types.Part(text=stakeholder_context)])
    
    # Every call uses the 'admin_id' to maintain session continuity
    events = runner.run_async(user_id=admin_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            # Returns a confirmation or immediate acknowledgment
            return event.content.parts[0].text

async def main():
    # 1. ARCHITECT DESIGN: The Strategic Mediator
    # Specifically instructed to look for contradictions and compromises.
    mediator = Agent(
        name="Boardroom_Mediator",
        instruction=(
            "You are a Senior Strategic Mediator. Your goal is to synthesize "
            "conflicting executive mandates. Analyze history for goal misalignment, "
            "identify risks of both paths, and propose a 'Third Way' consensus."
        ),
        model=get_model()
    )

    runner = get_runner(mediator)
    admin_user, session_id = await initialize_session() 
    
    print(f"--- [SYSTEM] Starting Executive Strategy Workshop | Session: {session_id} ---\n")
    
    # 2. THE WORKSHOP: Capture conflicting mandates
    # Turn 1: The Growth Perspective
    await record_executive_input(runner, session_id, admin_user, "CIO", 
        "We must deploy a private AI cluster by Q3 to maintain market parity. Delay is not an option.")
    
    # Turn 2: The Fiscal Perspective
    await record_executive_input(runner, session_id, admin_user, "CFO", 
        "The CAPEX budget is locked. We cannot authorize new hardware purchases until the 2027 fiscal cycle.")

    # 3. SYNTHESIS: Resolving the Deadlock
    # The agent now holds the "Tension" between Growth and Austerity in its context.
    synthesis_query = (
        "Summarize the primary conflict between the CIO and CFO. "
        "Provide a consensus recommendation that respects both the 'No CAPEX' rule "
        "and the 'Q3 AI readiness' requirement."
    )
    
    content_final = types.Content(role="user", parts=[types.Part(text=synthesis_query)])
    
    print("\n--- [MEDIATOR'S RECONCILED STRATEGY REPORT] ---")
    events = runner.run_async(user_id=admin_user, session_id=session_id, new_message=content_final)
    
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Workshop Session Failure: {e} ---")