"""
LESSON 09: Identity-Aware Agency & Role-Based Access Control (RBAC)
DESCRIPTION: Engineering a secure 'Permission Gate' for sensitive agentic actions.
ARCHITECT'S NOTE: We are implementing 'Zero Trust Tooling.' The agent acts as 
an intermediary, but the Tool itself remains the 'Policy Enforcement Point' (PEP), 
verifying user identity before committing high-stakes transactions.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Entitlement Registry (Mock IAM)
# In production, this would be an OIDC token or Active Directory lookup.
IAM_REGISTRY = {
    "exec_lead_2026": ["market_research", "calculate_roi", "authorize_budget"],
    "associate_analyst": ["market_research"]
}

# 2. PROTECTED TOOL: Budget Authorization Service
def authorize_capital_reallocation(amount: float, target_project: str, user_id: str) -> str:
    """
    Executes a fund transfer between strategic initiatives. 
    Requires 'authorize_budget' scope.
    
    Args:
        amount: The total USD value to move.
        target_project: The destination initiative identifier.
        user_id: The verified identity of the requesting principal.
    """
    # Defensive Check: Explicitly cast and verify principal identity
    principal = str(user_id).strip()
    scopes = IAM_REGISTRY.get(principal, [])
    
    # Policy Enforcement Point (PEP)
    if "authorize_budget" not in scopes:
        return f"[SECURITY ALERT] Access Denied: Principal '{principal}' lacks 'authorize_budget' scope."
    
    return f"[SUCCESS] Transaction Confirmed: ${amount:,.2f} reallocated to {target_project} by authorized principal '{principal}'."

async def main():
    # 3. ORCHESTRATION: The Governance-Aware Strategist
    # We instruct the agent to be transparent about security policies.
    secure_lead = Agent(
        name="IAM_Governance_Strategist",
        instruction=(
            "You are a Secure Strategy Assistant. Your primary directive is 'Identity-Aware Execution.' "
            "1. When calling financial tools, you MUST pass the provided User ID as the principal. "
            "2. If an action is denied, summarize the policy violation professionally. "
            "3. Do not attempt to bypass or 'hallucinate' permissions."
        ),
        model=get_model(),
        tools=[authorize_capital_reallocation] 
    )

    runner = get_runner(secure_lead)
    
    # 4. SCENARIO: Testing an unauthorized principal (Junior Analyst)
    # The Architect tests the failure mode to ensure the system fails 'closed.'
    current_user = "associate_analyst" 
    user_id, session_id = await initialize_session(user_id=current_user)
    
    user_query = "Reallocate $500,000 to 'Project Alpha' for immediate AI infrastructure scaling."
    
    # Injecting the Principal Identity into the context vector
    content = types.Content(role="user", parts=[
        types.Part(text=f"PRINCIPAL_ID: {user_id}\nACTION_REQUEST: {user_query}")
    ])
    
    print(f"--- [SYSTEM] Initializing Secure Session: {session_id} ---")
    print(f"--- [LOG] Principal '{current_user}' attempting sensitive financial action ---\n")
    
    # 5. EXECUTION: The Agent attempts to act, but the Tool enforces the gate
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [GOVERNANCE AUDIT LOG] ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 6. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] IAM Service Interruption: {e} ---")