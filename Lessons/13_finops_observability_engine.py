"""
LESSON 13: Usage Monitoring & Financial Observability
DESCRIPTION: Extracting token telemetry to calculate 'Cost per Insight.'
ARCHITECT'S NOTE: Intelligence has a price. By instrumenting our Agentic Runner 
with usage metadata, we provide the CFO with a deterministic view of 
operational spend, enabling 'Value-Based' model orchestration.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# ARCHITECT'S BENCHMARK: 2026 Model Unit Pricing
# Pricing reflects enterprise-grade tokens/sec and reliability.
COST_PER_1M_TOKENS_IN = 0.50  # Context injection cost
COST_PER_1M_TOKENS_OUT = 1.50 # Reasoning generation cost

async def main():
    # 1. ARCHITECT DESIGN: The Efficiency Lead
    # Instructed to balance depth with token economy.
    efficiency_lead = Agent(
        name="FinOps_Analyst",
        instruction=(
            "You are a Strategy Analyst focused on high-density insights. "
            "Analyze the inquiry with precision. Avoid 'Token Bloat'—ensure "
            "every word adds measurable strategic value."
        ),
        model=get_model()
    )

    runner = get_runner(efficiency_lead)
    user_id, session_id = await initialize_session()
    
    # 2. THE VECTOR: A Complex Regulatory Inquiry
    user_query = "Assess the 2026 Sovereign Cloud compliance risks for our North Atlantic data clusters."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Initializing Metered Analysis | Session: {session_id} ---")
    
    # 3. EXECUTION & TELEMETRY CAPTURE
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    async for event in events:
        if event.is_final_response():
            print("\n--- [STRATEGIC INTELLIGENCE] ---")
            print(event.content.parts[0].text)
            
            # 4. METADATA EXTRACTION: The FinOps Audit
            usage = event.usage_metadata
            p_tokens = usage.prompt_token_count
            c_tokens = usage.candidates_token_count
            total_tokens = p_tokens + c_tokens
            
            # Calculating precise TCO (Total Cost of Ownership)
            cost_in = (p_tokens / 1_000_000) * COST_PER_1M_TOKENS_IN
            cost_out = (c_tokens / 1_000_000) * COST_PER_1M_TOKENS_OUT
            total_cost = cost_in + cost_out
            
            print(f"\n" + "—"*40)
            print(f"FINOPS AUDIT | SESSION: {session_id}")
            print(f"Prompt (Input) Tokens:  {p_tokens:>8}")
            print(f"Candidate (Output) Tokens: {c_tokens:>8}")
            print(f"Total Token Weight:      {total_tokens:>8}")
            print(f"Calculated Insight Cost:  ${total_cost:.5f}")
            print("—"*40)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Observability Pipeline Fault: {e} ---")