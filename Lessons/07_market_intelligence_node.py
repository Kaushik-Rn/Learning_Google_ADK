"""
LESSON 07: Real-Time Intelligence & Tool Augmentation
DESCRIPTION: Integrating external telemetry sources to bypass LLM training cutoffs.
ARCHITECT'S NOTE: We are implementing a 'Data Augmentation' pattern. By connecting 
the agent to live industry vectors, we ensure strategic alignment with the 
2026 technical landscape.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Market Intelligence Tool (Async Pattern)
async def fetch_industry_intelligence(industry_vector: str) -> str:
    """
    Retrieves high-fidelity innovation trends and competitive differentiators 
    for a specific industrial sector.
    
    Args:
        industry_vector: The specific sector (e.g., 'Banking', 'Healthcare').
    """
    # Defensive programming: Normalizing the input vector
    sector = str(industry_vector).strip().title()
    
    # Simulation of a high-latency API call (e.g., Tavily, Serper, or Internal RAG)
    intelligence_vault = {
        "Banking": "2026 SHIFT: Transition from 'Mobile-First' to 'Agentic-First' banking. Differentiator: Sovereign AI agents for hyper-personalized asset management.",
        "Supply Chain": "2026 SHIFT: Autonomous mesh networks for logistics. Differentiator: Predictive self-healing supply chains.",
        "Healthcare": "2026 SHIFT: Generative Diagnostic Co-pilots. Differentiator: Sub-second clinical decision support (CDS) integration."
    }
    
    data_payload = intelligence_vault.get(sector, "TREND DETECTED: Cross-sector acceleration of Agentic AI Orchestration Layers.")
    return f"[EXTERNAL DATA SOURCE] Intelligence for {sector}: {data_payload}"

async def main():
    # 2. ORCHESTRATION: The Market Intelligence Lead
    # We move beyond 'answering' to 'synthesizing' opportunity vs. threat.
    market_lead = Agent(
        name="MarketIntelligence_Analyst",
        instruction=(
            "You are a Senior Market Intelligence Analyst for the CIO's Office. "
            "Your mission: Fetch live industry telemetry and synthesize it into a "
            "high-density 'Strategic Pivot' summary. "
            "PROTOCOL: You MUST use the 'fetch_industry_intelligence' tool for any industry-specific query. "
            "OUTPUT STRUCTURE: 1. Current Shift | 2. Strategic Differentiator | 3. CIO Opportunity vs. Threat."
        ),
        model=get_model(),
        tools=[fetch_industry_intelligence] 
    )

    runner = get_runner(market_lead)
    user_id, session_id = await initialize_session()
    
    # 3. RESEARCH VECTOR: Targeting a 2026-specific trend
    user_query = "What is the primary technical differentiator in the Banking sector for 2026 AI roadmaps?"
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Initializing Intelligence Fetch | Session: {session_id} ---")
    print(f"--- [LOG] Triggering External Research Loop for: {user_query} ---\n")
    
    # 4. EXECUTION: Bridging Llama 3.2 with live tool outputs
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [REAL-TIME STRATEGIC RESEARCH BRIEF] ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Intelligence Pipeline Failure: {e} ---")