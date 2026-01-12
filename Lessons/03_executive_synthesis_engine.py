"""
LESSON 03: Executive Synthesis & Schema Enforcement
DESCRIPTION: Utilizing strict templating to convert high-entropy AI reasoning into low-latency executive memos.
ARCHITECT'S NOTE: We are moving from 'Conversational AI' to 'Deterministic Output Formatting.'
By enforcing a schema, we ensure the agent functions as a reliable reporting microservice.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: The Chief of Staff Specialist
    # We define the "Communication Guardrails" in the system instruction.
    synthesis_lead = Agent(
        name="ChiefOfStaff_Specialist",
        instruction=(
            "You are a Strategy Chief of Staff for a Fortune 500 CIO. "
            "Your mission is to distill complex technological shifts into high-density, "
            "low-word-count executive memos. Avoid fluff. Prioritize strategic impact and risk."
        ),
        model=get_model()
    )

    runner = get_runner(synthesis_lead)
    user_id, session_id = await initialize_session()
    
    # 2. ARCHITECTURAL TEMPLATE: Schema-Driven Prompting
    # Defining a 'Contract' between the user and the agent.
    analysis_vector = "The transition from Robotic Process Automation (RPA) to Agentic AI"
    
    # Using a structured f-string as a 'System Contract'
    memo_schema = f"""
    [MISSION CRITICAL ANALYSIS REQUEST]: {analysis_vector}
    
    INSTRUCTION: Execute analysis and populate the following schema exactly:
    
    ## 📋 EXECUTIVE SUMMARY
    (Two-sentence high-level strategic positioning)
    
    ## 🔄 ARCHITECTURAL SHIFT: RPA VS. AGENTIC
    (Contrast 'If-Then' logic vs. 'Goal-Oriented' autonomy)
    
    ## 🎯 STRATEGIC RECOMMENDATION
    (One singular, high-leverage action item for the current fiscal year)
    
    ## ⚠️ KEY RISK VECTOR
    (The primary technical or cultural barrier to execution)
    """

    content = types.Content(role="user", parts=[types.Part(text=memo_schema)])
    
    print(f"--- [SYSTEM] Session {session_id}: Synthesizing Executive Intelligence ---")
    print(f"--- [LOG] Enforcing Schema-Driven Output Format ---\n")
    
    # 3. EXECUTION: Streaming the synthesized intelligence
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [CONFIDENTIAL EXECUTIVE MEMO] ---")
    async for event in events:
        if event.is_final_response():
            # The Architect ensures the output is presentation-ready
            print(event.content.parts[0].text)

    # 4. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] System Fault in Synthesis Engine: {e} ---")