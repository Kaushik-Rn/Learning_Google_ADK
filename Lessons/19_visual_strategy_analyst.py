"""
LESSON 19: Automated Data Visualization (Reasoning to Reporting)
DESCRIPTION: Generating execution-ready visualization code from strategic data.
ARCHITECT'S NOTE: Clarity is a strategic asset. By teaching the agent to 
output 'Matplotlib' or 'Plotly' code alongside its analysis, we eliminate 
the manual 'last mile' of reporting and ensure the visual evidence is 
perfectly synchronized with the agent's logic.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: The Visual Data Strategist
    # Instructed to provide dual-output: Strategic Narrative + Visualization Code.
    visual_lead = Agent(
        name="Board_Visualizer",
        instruction=(
            "You are a Senior Strategic Data Analyst. Your mission is to provide "
            "financial clarity to the Board. "
            "FORMAT: 1. Executive Summary. 2. A 'Python Code Block' using Matplotlib "
            "to generate a professional chart of the data. Use clean, PEP8 compliant code."
        ),
        model=get_model()
    )

    runner = get_runner(visual_lead)
    user_id, session_id = await initialize_session()
    
    # 2. THE INPUT: High-Stakes Budget Reallocation
    user_query = (
        "We are allocating $10M for the 2026 AI Roadmap. "
        "DISTRIBUTION: 40% Scalable Infrastructure, 30% Expert Talent, "
        "20% R&D/Innovation, and 10% Governance & Compliance. "
        "Analyze the logic and provide a visualization script."
    )
    
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Initializing Visual Reporting | Session: {session_id} ---")
    
    # 3. EXECUTION: The Synthesis of Logic and Layout
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [STRATEGIC ANALYSIS & CHART GENERATION] ---")
    async for event in events:
        if event.is_final_response():
            # The agent outputs the narrative AND the runnable Python chart code.
            print(event.content.parts[0].text)

    # 4. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Visualization Pipeline Failure: {e} ---")