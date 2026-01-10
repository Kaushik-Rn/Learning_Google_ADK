"""
LESSON 01: Infrastructure Control Plane
DESCRIPTION: Establishing the high-availability bridge between Google ADK and local compute (Ollama).
ARCHITECT'S NOTE: This verifies the 'Control Plane' connectivity. We utilize the 'cleanup' 
utility as a lifecycle management pattern to ensure session atomicity.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: Instantiate the Infrastructure Auditor
    # Naming convention: {Role}_{Specialty} to define domain boundaries.
    infrastructure_auditor = Agent(
        name="InfraAuditor_Lead",
        instruction=(
            "You are the Lead Infrastructure Auditor for the CIO Office. "
            "Your mission: Synthesize technical architectural benefits into high-level "
            "executive strategic vectors. Maintain a tone of technical authority."
        ),
        model=get_model() # Configured for Ollama / Llama 3.2
    )

    # 2. ORCHESTRATION: Initialize the Execution Runner
    runner = get_runner(infrastructure_auditor)
    
    # 3. STATE MANAGEMENT: Register the Global Session State
    # This 'Check-in' pattern ensures observability across the agentic lifecycle.
    user_id, session_id = await initialize_session()
    
    # 4. INPUT VECTOR: Constructing Type-Safe Payload
    # Moving beyond 'strings' to structured Content objects for future multi-modal scaling.
    strategic_query = "Analyze the ROI of Google ADK vs. monolithic LLM wrappers for a 2026 enterprise roadmap."
    content = types.Content(role="user", parts=[types.Part(text=strategic_query)])
    
    print(f"--- [SYSTEM] Session ID: {session_id} | Status: ACTIVE ---")
    print(f"--- [LOG] Routing to Local Compute Brain (Ollama: Llama 3.2) ---\n")
    
    # 5. EXECUTION: Asynchronous Stream Processing
    # We treat the run as an event stream, allowing for real-time architectural telemetry.
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [EXECUTIVE INTELLIGENCE OUTPUT] ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 6. LIFECYCLE MANAGEMENT: Graceful Teardown
    # Critical for clearing local buffer and terminating Ollama socket connections.
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- [SYSTEM] Manual Interrupt Detected. Forcing Cleanup. ---")