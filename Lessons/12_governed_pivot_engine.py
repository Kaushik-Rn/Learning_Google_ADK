"""
LESSON 12: Human-in-the-Loop (HITL) & Managed Governance
DESCRIPTION: Establishing a synchronous 'Approval Gate' for high-impact strategic shifts.
ARCHITECT'S NOTE: We are implementing a 'Draft-Review-Finalize' pattern. 
This prevents 'Autonomous Drift' and ensures that every AI-generated pivot 
is anchored by human accountability and organizational nuance.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: The Staff Advisor
    # Explicitly told that its output is a 'Draft' subject to veto.
    pivot_staff = Agent(
        name="Strategic_Draft_Specialist",
        instruction=(
            "You are a Strategy Staff Assistant. Your role is to propose 'Bold Pivots' "
            "based on data, but you MUST acknowledge that your output is a DRAFT. "
            "Always provide a justification that a human executive can audit."
        ),
        model=get_model()
    )

    runner = get_runner(pivot_staff)
    user_id, session_id = await initialize_session()
    
    # 2. STAGE 1: The Autonomous Hypothesis
    print(f"--- [SYSTEM] Initializing Decision Support | Session: {session_id} ---")
    user_query = "We need to reallocate $1M from the IT budget for an emergency AI scaling initiative. Propose a cut."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [LOG] Agent generating Strategic Draft... ---")
    
    draft_proposal = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    async for event in events:
        if event.is_final_response():
            draft_proposal = event.content.parts[0].text

    print(f"\n--- [AI DRAFT PROPOSAL] ---\n{draft_proposal}\n")

    # 3. STAGE 2: THE GOVERNANCE GATEWAY (HITL)
    # This represents the 'Policy Enforcement Point' where human intuition is injected.
    print("--- [WAITING FOR EXECUTIVE REVIEW] ---")
    print("Action: Enter 'APPROVE' or provide specific feedback/constraints:")
    human_feedback = input("Executive Input > ")

    # 4. STAGE 3: Contextual Refinement
    # The agent reconciles its logic with the human's subjective feedback.
    if human_feedback.upper() == "APPROVE":
        final_instruction = "The proposal is approved. Generate the final board-ready summary with an implementation timeline."
    else:
        final_instruction = (
            f"The proposal was REJECTED/MODIFIED by the human lead with this feedback: '{human_feedback}'. "
            "Incorporate this nuance and generate a revised strategic memo."
        )

    content_final = types.Content(role="user", parts=[types.Part(text=final_instruction)])
    
    print("\n--- [GENERATING FINAL GOVERNED OUTPUT] ---")
    events_final = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_final)
    async for event in events_final:
        if event.is_final_response():
            print(f"\n--- [FINAL BOARD-READY MEMO] ---\n{event.content.parts[0].text}")

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Governance Pipeline Fault: {e} ---")