"""
LESSON 16: Strategic Session Branching (Multiverse Simulation)
DESCRIPTION: Creating parallel reasoning tracks from a shared foundational context.
ARCHITECT'S NOTE: We are implementing 'Contextual Forking.' By seeding a 
primary session with core business constraints and then branching into 
parallel tasks, we enable deterministic comparison of 'What-If' scenarios.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def execute_scenario_branch(runner, user_id, session_id, scenario_id, vector_prompt):
    """
    Architectural Task: Forks the shared context into a specific strategic vector.
    """
    print(f"--- [BRANCHING] Initializing Vector: {scenario_id} ---")
    
    content = types.Content(role="user", parts=[types.Part(text=vector_prompt)])
    
    # We use the shared session_id to inherit the 'Foundation' context
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    
    payload = ""
    async for event in events:
        if event.is_final_response():
            payload = event.content.parts[0].text
            
    return f"--- [SCENARIO OUTCOME: {scenario_id}] ---\n{payload}\n"

async def main():
    # 1. ARCHITECT DESIGN: The Scenario Planner
    # Instructed to maintain consistency with the 'Foundation' while exploring the 'Branch'.
    planner = Agent(
        name="Scenario_Multiverse_Lead",
        instruction=(
            "You are a Strategic Risk Consultant. Your role is to take foundational "
            "business goals and stress-test them against specific 'What-If' variables. "
            "Compare every outcome against the original ROI and risk benchmarks."
        ),
        model=get_model()
    )

    runner = get_runner(planner)
    user_id, main_session_id = await initialize_session()
    
    # 2. SEEDING THE FOUNDATION: Establishing the 'Ground Truth'
    # This context will be inherited by all subsequent branches.
    foundation_context = (
        "GOAL: Modernize global Data Centers for AI readiness by Q4 2027. "
        "CONSTRAINTS: $5M fixed capital expenditure. TARGET: 30% latency reduction."
    )
    
    print(f"--- [SYSTEM] Seeding Strategic Foundation | Session: {main_session_id} ---")
    
    # We perform a 'silent seed' to prime the session memory
    seed_event = await runner.run_async(
        user_id=user_id, 
        session_id=main_session_id, 
        new_message=types.Content(role="user", parts=[types.Part(text=foundation_context)])
    ).__anext__() 

    # 3. BRANCHING: Defining the Multiverse Vectors
    # We define different variables to apply to the same foundation.
    scenarios = [
        ("ACCELERATED", "Variable: Move deadline to Q4 2026. Increase budget by $2M. Analyze Risk."),
        ("AUSTERITY", "Variable: Reduce budget by 40%. Maintain 2027 deadline. Analyze ROI impact."),
        ("EDGE_PIVOT", "Variable: Pivot 25% of CAPEX to regional Edge nodes instead of Core DC. Analyze Latency.")
    ]

    # 4. CONCURRENCY: Executing the Multiverse
    print(f"--- [LOG] Executing {len(scenarios)} parallel scenario forks... ---\n")
    
    simulation_tasks = [
        execute_scenario_branch(runner, user_id, main_session_id, name, prompt) 
        for name, prompt in scenarios
    ]
    
    # Gathering results into a unified strategic board report
    strategic_outcomes = await asyncio.gather(*simulation_tasks)

    # 5. SYNTHESIS: Displaying the Comparative Matrix
    for outcome in strategic_outcomes:
        print(outcome)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Scenario Engine Fault: {e} ---")