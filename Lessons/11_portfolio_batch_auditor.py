"""
LESSON 11: Asynchronous Batching & High-Throughput Auditing
DESCRIPTION: Utilizing 'asyncio.gather' to execute concurrent strategic vetting.
ARCHITECT'S NOTE: We are moving from 'Conversational Latency' to 'Batch Efficiency.' 
By parallelizing the execution, we can audit an entire project portfolio in 
O(1) time relative to a single request, maximizing infrastructure utilization.
"""

import asyncio
import time
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def execute_strategic_audit(runner, user_id, session_id, project_name, draft_text):
    """
    Architectural Task: Performs a single-turn audit on an isolated task thread.
    """
    audit_query = (
        f"CRITICAL AUDIT REQUEST for {project_name}. "
        f"PROPOSAL: {draft_text} "
        "Analyze for: 1. ROI Potential, 2. Technical Debt Risk, 3. 2026 Strategic Fit. "
        "Format: Bulleted High-Density Brief."
    )
    
    content = types.Content(role="user", parts=[types.Part(text=audit_query)])
    
    final_payload = ""
    # Every audit runs as its own async event stream
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            final_payload = event.content.parts[0].text
            
    return f"--- [AUDIT REPORT: {project_name}] ---\n{final_payload}\n"

async def main():
    # 1. ARCHITECT DESIGN: The High-Throughput Auditor
    auditor_lead = Agent(
        name="Portfolio_Vetting_Specialist",
        instruction=(
            "You are a Senior Portfolio Auditor for the CIO. "
            "Your tone is objective, analytical, and brief. "
            "Identify 'Strategic Misalignment' immediately if found."
        ),
        model=get_model()
    )

    runner = get_runner(auditor_lead)
    user_id, session_id = await initialize_session()
    
    # 2. DATA VECTOR: The 2026 Innovation Portfolio
    # We represent these as a dictionary for clean iteration.
    portfolio_manifest = {
        "Project_Zodiac": "Migrate core banking data to a sovereign cloud in the EU for GDPR 2026 compliance.",
        "Project_Quantum": "Deploy LLM-driven predictive maintenance for global manufacturing hubs.",
        "Project_Nexus": "Enterprise-wide transition from traditional RPA to Agentic AI Orchestration."
    }
    
    print(f"--- [SYSTEM] Initializing Batch Audit for {len(portfolio_manifest)} Initiatives ---")
    start_benchmark = time.perf_counter()

    # 3. CONCURRENCY CONTROL: Building the Task Queue
    # We 'fire' all requests simultaneously rather than waiting for responses.
    audit_queue = [
        execute_strategic_audit(runner, user_id, session_id, name, desc) 
        for name, desc in portfolio_manifest.items()
    ]
    
    # Executing the 'Fan-Out' pattern
    audit_results = await asyncio.gather(*audit_queue)
    
    # 4. DATA AGGREGATION
    for report in audit_results:
        print(report)

    execution_time = time.perf_counter() - start_benchmark
    print(f"--- [SYSTEM] Portfolio Audit Completed in {execution_time:.2f} seconds. ---")

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Batch Processor Failure: {e} ---")