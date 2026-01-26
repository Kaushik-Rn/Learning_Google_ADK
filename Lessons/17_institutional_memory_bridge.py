"""
LESSON 17: Long-Term Memory & Institutional RAG
DESCRIPTION: Implementing a 'Lessons Learned' retrieval loop to inform future strategy.
ARCHITECT'S NOTE: We are moving from 'Zero-Shot' to 'Context-Enriched' reasoning. 
By forcing the agent to interrogate a historical Post-Mortem database, we 
transform the model from a generic consultant into a veteran company insider.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Post-Mortem Retrieval Tool
# This acts as the bridge to your organization's 'Failure & Success' archives.
async def query_historical_post_mortems(strategic_domain: str) -> str:
    """
    Retrieves internal records of past project failures, audits, and lessons learned.
    
    Args:
        strategic_domain: The area of inquiry (e.g., 'Cloud', 'Data', 'Cybersecurity').
    """
    # Simulated Proprietary Knowledge Base
    # In production, this would be a vector search across PDF/Docx project retrospectives.
    historical_archives = {
        "Cloud": (
            "CRITICAL FAILURE (2023): 'Project Sky-High' exceeded budget by 45%. "
            "ROOT CAUSE: Unmonitored egress costs and lack of cross-region optimization."
        ),
        "Data": (
            "AUDIT FINDING (2024): 60% of Data Lake content deemed 'Rot/Dark Data'. "
            "LESSON: Mandatory tagging at ingestion is required for 2026 AI readiness."
        ),
        "Infrastructure": (
            "EXECUTIVE NOTE (2022): Technical debt in legacy ERP prevented API-first migration. "
            "REACTION: All new builds must be headless/decoupled."
        )
    }
    
    # Normalizing the lookup key
    key = strategic_domain.strip().capitalize()
    record = historical_archives.get(key, "NO PREVIOUS RECORD: Proceed with standard industry caution.")
    
    return f"[INTERNAL ARCHIVE - {key}] {record}"

async def main():
    # 2. ORCHESTRATION: The Historical Strategist
    # This persona is tuned to be 'Risk-Averse' based on historical data.
    wise_strategist = Agent(
        name="Historical_Memory_Strategist",
        instruction=(
            "You are a Senior CIO Advisor with access to the company's Historical Archives. "
            "MANDATE: Before proposing any strategy, you MUST invoke 'query_historical_post_mortems'. "
            "If the archive reveals a past failure, you MUST explicitly address how your 2026 "
            "recommendation prevents a recurrence of that specific root cause."
        ),
        model=get_model(),
        tools=[query_historical_post_mortems]
    )

    runner = get_runner(wise_strategist)
    user_id, session_id = await initialize_session()
    
    # 3. THE INQUIRY: Attempting a high-stakes expansion
    user_query = "Draft a roadmap for our 2026 Multi-Cloud Data Expansion initiative."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Establishing Historical Context Bridge | Session: {session_id} ---")
    print(f"--- [LOG] Interrogating 'Cloud' and 'Data' archives for lessons learned... ---\n")
    
    # 4. EXECUTION: The Agent synthesizes 2026 tech with 2023 lessons
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [HISTORICALLY-INFORMED STRATEGY MEMO] ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Archive Retrieval Interruption: {e} ---")