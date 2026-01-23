"""
LESSON 14: Agentic Unit Testing & Evaluation (LLM-as-a-Judge)
DESCRIPTION: Engineering a test suite to validate non-deterministic agent outputs.
ARCHITECT'S NOTE: We are implementing 'Contract-Based Testing.' By treating the 
agent's output as a response payload that must satisfy a predefined schema and 
tone, we ensure the CIO's office receives consistent, board-ready intelligence.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def validate_agent_contract(test_name, query, success_criteria):
    """
    Executes a test vector and validates the output against a Strategic Contract.
    """
    print(f"[TESTING] {test_name}...")
    
    # 1. SETUP: The Subject under Test
    strategy_subject = Agent(
        name="Strategy_Vetting_Subject",
        instruction=(
            "You are a Senior CIO Advisor. You must include a 'FINANCIAL IMPACT' "
            "and a 'STRATEGIC RISK' section in every response. Maintain a "
            "formal, data-driven tone."
        ),
        model=get_model()
    )
    
    runner = get_runner(strategy_subject)
    user_id, session_id = await initialize_session()
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # 2. INFERENCE: Captured within the testing harness
    response_payload = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    async for event in events:
        if event.is_final_response():
            response_payload = event.content.parts[0].text

    # 3. VERIFICATION: Checking for Contract Fulfillment
    results = {"passed": True, "violations": []}
    
    for marker in success_criteria:
        if marker.lower() not in response_payload.lower():
            results["passed"] = False
            results["violations"].append(f"Missing Required Section: '{marker}'")
    
    # 4. REPORTING
    status = "✅ PASSED" if results["passed"] else "❌ FAILED"
    print(f"--- [RESULT: {status}] ---")
    if results["violations"]:
        for v in results["violations"]: print(f"   ! {v}")
    print("—" * 40)
    
    return results["passed"]

async def main():
    # ARCHITECT'S TEST SUITE: Defining the Strategic Benchmarks
    evaluation_suite = [
        {
            "name": "Fiscal Rigor Test",
            "query": "Evaluate the move to a multi-cloud strategy for 2026.",
            "criteria": ["FINANCIAL IMPACT", "ROI", "Cloud"]
        },
        {
            "name": "Governance Tone Check",
            "query": "Assess the performance of our current AI ethics committee.",
            "criteria": ["STRATEGIC RISK", "Compliance"]
        }
    ]

    print(f"--- [SYSTEM] Starting Agentic QA Lab | 2026 Strategy Standards ---")
    
    test_results = []
    for test in evaluation_suite:
        success = await validate_agent_contract(test["name"], test["query"], test["criteria"])
        test_results.append(success)

    # 5. FINAL AUDIT
    passed_count = sum(test_results)
    total_count = len(evaluation_suite)
    print(f"--- [LAB SUMMARY] Final Quality Score: {passed_count}/{total_count} ---")
    
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Lab Pipeline Failure: {e} ---")