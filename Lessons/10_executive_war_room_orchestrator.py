"""
LESSON 10: Multi-Agent Adversarial Collaboration
DESCRIPTION: Engineering a high-fidelity 'War Room' simulation to eliminate AI bias.
ARCHITECT'S NOTE: We are moving from 'Linear Prompting' to 'Relational Orchestration.' 
By defining agents with conflicting KPIs (Growth vs. Risk), we create a 
self-correcting intelligence loop that mimics executive decision-making.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: Defining the "Conflict Personas"
    # Agent 1: The Exponential Growth Lead
    innovator = Agent(
        name="Growth_Orchestrator",
        instruction=(
            "You are the Chief Innovation Officer. Your mission is to maximize "
            "market disruption and speed-to-market. Ignore costs; focus on competitive MOAT."
        ),
        model=get_model()
    )

    # Agent 2: The Fiscal Risk Lead
    cfo = Agent(
        name="Risk_Audit_Specialist",
        instruction=(
            "You are a Skeptical CFO. Your mission is to identify technical debt, "
            "operational risk, and ROI leakage. Challenge every growth assumption."
        ),
        model=get_model()
    )

    # 2. STATE INITIALIZATION
    user_id, session_id = await initialize_session()
    proposal = "Decommission 100% of human-led customer support in favor of Agentic AI by Q1 2026."
    
    print(f"--- [SYSTEM] Initializing Strategic War Room | Session: {session_id} ---")
    print(f"--- [PROPOSAL] {proposal} ---\n")

    # --- PHASE 1: The Innovation Pitch ---
    # Capturing the 'Pro' vector
    runner_inv = get_runner(innovator)
    content_inv = types.Content(role="user", parts=[types.Part(text=f"Draft a high-impact pitch for: {proposal}")])
    pitch_payload = ""
    
    print("🚀 [ACTION] Growth_Orchestrator drafting the Innovation Case...")
    async for event in runner_inv.run_async(user_id=user_id, session_id=session_id, new_message=content_inv):
        if event.is_final_response():
            pitch_payload = event.content.parts[0].text
    
    # --- PHASE 2: The Fiscal Rebuttal ---
    # Handing off the 'Pro' vector to the 'Con' agent for critique
    runner_cfo = get_runner(cfo)
    content_cfo = types.Content(role="user", parts=[types.Part(text=f"Perform a ruthless risk audit on this pitch: {pitch_payload}")])
    audit_payload = ""

    print("⚖️ [ACTION] Risk_Audit_Specialist executing Fiscal Stress-Test...")
    async for event in runner_cfo.run_async(user_id=user_id, session_id=session_id, new_message=content_cfo):
        if event.is_final_response():
            audit_payload = event.content.parts[0].text

    # --- PHASE 3: The Board Synthesis (CEO) ---
    # Final 'Policy Enforcement' agent to reconcile the two views
    ceo_synthesizer = Agent(
        name="Executive_Decision_Lead", 
        instruction="Review the following debate. Provide a final 'Go/No-Go' recommendation with three mandatory mitigation steps.", 
        model=get_model()
    )
    runner_ceo = get_runner(ceo_synthesizer)
    
    final_debate_vector = f"INNOVATION CASE: {pitch_payload}\n\nFISCAL AUDIT: {audit_payload}"
    content_final = types.Content(role="user", parts=[types.Part(text=final_debate_vector)])
    
    print("\n--- [FINAL EXECUTIVE RECONCILIATION] ---")
    async for event in runner_ceo.run_async(user_id=user_id, session_id=session_id, new_message=content_final):
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 3. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] War Room Orchestration Failure: {e} ---")