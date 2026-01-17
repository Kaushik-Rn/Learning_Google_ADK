"""
LESSON 08: Contextual Grounding via MCP (Model Context Protocol) Pattern
DESCRIPTION: Bridging the "Knowledge Gap" by connecting agents to private, high-fidelity internal data.
ARCHITECT'S NOTE: We are implementing a 'Secure Gateway' pattern. The agent is forced 
to ground its reasoning in the 'Strategy Knowledge Base' (SKB) before synthesizing 
advice, preventing generic hallucinations and ensuring corporate alignment.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Internal Knowledge Base (SKB) Connector
# This simulates an MCP-compliant server querying a Vector Store or SQL DB.
async def query_internal_strategy_skb(resource_key: str) -> str:
    """
    Queries the private Strategy Knowledge Base for real-time project telemetry, 
    internal KPIs, and resource allocation status.
    
    Args:
        resource_key: The internal project identifier or KPI metric name.
    """
    # Defensive normalization of the lookup key
    lookup = str(resource_key).replace(" ", "_").title()
    
    # Mocking a secure internal repository
    internal_skb = {
        "Project_Alpha": "Status: CRITICAL/DELAYED. Risk: Legacy API bottleneck. Budget: $1.2M utilized.",
        "Cloud_Migration": "Status: OPTIMIZED. Savings: $300k YTD. Infrastructure: 65% Serverless transition.",
        "Cyber_Shield": "Status: PROTOTYPING. Priority: P0 (Executive Mandate). Launch: Q3 2026."
    }
    
    data_entry = internal_skb.get(lookup, "NULL: No internal record found. Exercise caution.")
    return f"[INTERNAL DATA SOURCE - SECURE] {lookup}: {data_entry}"

async def main():
    # 2. ORCHESTRATION: The Strategic Resource Auditor
    # This agent treats internal data as the primary "Truth Vector."
    resource_auditor = Agent(
        name="Internal_Resource_Auditor",
        instruction=(
            "You are a Strategic Resource Auditor for the CIO. "
            "Your mission: Perform resource reconciliation by comparing internal project status "
            "against corporate goals. "
            "PROTOCOL: You MUST invoke 'query_internal_strategy_skb' for any mention of "
            "internal projects or KPIs. Prioritize the returned [INTERNAL DATA] over "
            "your general training knowledge for final recommendations."
        ),
        model=get_model(),
        tools=[query_internal_strategy_skb] 
    )

    runner = get_runner(resource_auditor)
    user_id, session_id = await initialize_session()
    
    # 3. INTERNAL DATA INQUIRY: A high-stakes resource reallocation query
    user_query = "Assess the viability of shifting senior engineering resources from Project Alpha to the Cloud Migration initiative."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Establishing Secure SKB Bridge | Session: {session_id} ---")
    print(f"--- [LOG] Interrogating Private Data Store for Resource Key: 'Project Alpha' ---\n")
    
    # 4. EXECUTION: The Agent reconciles model reasoning with private telemetry
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [INTERNAL STRATEGIC RECOMMENDATION] ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Internal Data Bridge Failure: {e} ---")