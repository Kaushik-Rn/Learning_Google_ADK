"""
LESSON 18: Dynamic Persona Switching & Risk Profiling
DESCRIPTION: Adapting agent heuristics based on departmental constraints.
ARCHITECT'S NOTE: We are implementing 'Contextual Heuristics.' By wrapping 
the agent's core logic in a departmental persona, we ensure that 'Innovation' 
requests get disruptive advice while 'Compliance' requests get defensive audits.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Persona Registry
# This defines the 'Core Values' and 'Risk Thresholds' for each business unit.
PERSONA_CONFIG = {
    "Innovation_Lab": {
        "role": "Disruptive Founder",
        "instruction": "MANDATE: Speed and Disruption. Prioritize competitive advantage and market capture over stability. Encourage 'Fast Failure'."
    },
    "Compliance_Finance": {
        "role": "Chief Risk Auditor",
        "instruction": "MANDATE: Stability and Governance. Prioritize regulatory adherence, audit trails, and zero-downtime. Identify all potential failure modes."
    },
    "Default": {
        "role": "General Strategist",
        "instruction": "MANDATE: Balanced Growth. Provide a moderate analysis of risk vs. reward."
    }
}

async def execute_specialized_consult(business_unit: str, inquiry: str):
    """
    Dynamically constructs a specialized agent based on the departmental persona.
    """
    config = PERSONA_CONFIG.get(business_unit, PERSONA_CONFIG["Default"])
    
    # 2. INJECTION: Wrapping the Agent in its Departmental Persona
    agent = Agent(
        name=f"Strategist_{business_unit}",
        instruction=(
            f"You are the {config['role']} for the organization. {config['instruction']} "
            "Ensure your final recommendation reflects these specific departmental values."
        ),
        model=get_model()
    )

    runner = get_runner(agent)
    user_id, session_id = await initialize_session()
    
    content = types.Content(role="user", parts=[types.Part(text=inquiry)])
    
    print(f"--- [SYSTEM] Activating Persona: {config['role']} | Unit: {business_unit} ---")
    
    response_payload = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            response_payload = event.content.parts[0].text
            
    print(f"--- [ADVICE FOR {business_unit}] ---\n{response_payload}\n")

async def main():
    # 3. SCENARIO: One Request, Two Realities
    # High-risk inquiry: Implementing an unproven Beta-version AI Gateway.
    strategic_inquiry = "Should we deploy the unproven Beta-version of the 'Neural-Flow' AI Gateway today?"
    
    # Witness the strategic delta
    await execute_specialized_consult("Innovation_Lab", strategic_inquiry)
    await execute_specialized_consult("Compliance_Finance", strategic_inquiry)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Persona Factory Failure: {e} ---")