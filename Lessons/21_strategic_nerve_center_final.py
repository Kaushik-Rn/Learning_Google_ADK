"""
LESSON 21: The Strategic Executive Dashboard (Full Integration)
DESCRIPTION: The Grand Finale. A production-ready blueprint combining 
Tool Calling, Institutional Memory (RAG), and Executive Mediation.
ARCHITECT'S NOTE: This is the culmination of 'Session Sovereignty.' We are 
building a high-confidence system where every recommendation is backed by 
precision math, historical precedent, and reconciled stakeholder logic.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# --- 1. THE ENTERPRISE TOOLSET ---

def calculate_precision_roi(investment: str, projected_savings: str) -> str:
    """Performs deterministic financial validation to avoid LLM hallucination."""
    try:
        inv = float(investment)
        sav = float(projected_savings)
        if inv <= 0: return "Error: Investment base must be positive."
        
        roi_pct = ((sav - inv) / inv) * 100
        return f"[FINANCIAL AUDIT] ROI: {roi_pct:.2f}% | Net Gain: ${sav - inv:,.2f}"
    except (ValueError, TypeError):
        return "Error: Non-numeric financial data provided."

async def fetch_institutional_archives(topic: str) -> str:
    """Retrieves historical 'scars and successes' from the organizational memory."""
    archive = {
        "AI Gateway": "2024 RETROSPECTIVE: Centralization reduced sprawl by 35% but hit 200ms latency bottlenecks."
    }
    return archive.get(topic, "No previous data found. Recommend a Pilot Phase.")

async def main():
    # --- 2. ARCHITECT DESIGN: The Master Orchestrator ---
    # The 'Senior Strategic Lead' persona with full tool access.
    master_strategist = Agent(
        name="Global_CIO_Advisor",
        instruction=(
            "You are the Lead Strategic Advisor for the Office of the CIO. "
            "For every request: 1. Audit finances via 'calculate_precision_roi'. "
            "2. Inoculate the plan using 'fetch_institutional_archives'. "
            "3. Reconcile conflicting stakeholder perspectives into a single 'Go/No-Go' verdict."
        ),
        model=get_model(),
        tools=[calculate_precision_roi, fetch_institutional_archives]
    )

    runner = get_runner(master_strategist)
    admin_id, session_id = await initialize_session()
    
    # --- 3. THE DOSSIER: Multi-Variable Integration ---
    # A single context packet containing conflict, math, and direction.
    strategic_dossier = """
    PROPOSAL: '2026 Enterprise AI Gateway'
    FINANCIALS: $3,000,000 Investment | $6,500,000 Efficiency Savings.
    CIO PERSPECTIVE: 'Urgent need for governance of autonomous agents.'
    CFO PERSPECTIVE: 'Concerned about high upfront costs and the memory of 2024's delays.'
    
    ACTION: Perform a full-spectrum audit and provide a final Board recommendation.
    """
    
    print(f"--- [SYSTEM] Activating Executive Nerve Center | Session: {session_id} ---")
    
    content = types.Content(role="user", parts=[types.Part(text=strategic_dossier)])
    
    # --- 4. THE GRAND EXECUTION ---
    print("\n--- [LOG] Running Financial Audit, Memory Retrieval, and Mediation Loop... ---")
    
    events = runner.run_async(user_id=admin_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            print("\n" + "█"*60)
            print("         OFFICE OF THE CIO: FINAL STRATEGIC VERDICT         ")
            print("█"*60)
            print(event.content.parts[0].text)
            
            # Final Metrics Observability
            usage = event.usage_metadata
            print(f"\n[TELEMETRY] Total Session Weight: {usage.total_token_count} tokens.")

    await cleanup()
    print(f"\n--- [COMPLETED] 21-Day ADK Masterclass Series | Architecture Finalized ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [SYSTEM ERROR] Nerve Center Failure: {e} ---")