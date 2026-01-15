"""
LESSON 06: Deterministic Tool Integration (Function Calling)
DESCRIPTION: Bridging the gap between probabilistic reasoning and exact mathematical execution.
ARCHITECT'S NOTE: We are implementing a 'Trusted Tool' pattern. The LLM handles the 
intent recognition, but delegates the computation to a hardened Python function 
to eliminate hallucinated metrics.
"""


import asyncio
import ast
import inspect
import re
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. ARCHITECT DESIGN: The Atomic Financial Tool
# THE TOOL: Deterministic Microservice
def run_math_calculation(cap_ex: float, annual_opex_savings: float) -> dict:
    roi = ((annual_opex_savings - cap_ex) / cap_ex) * 100
    payback = cap_ex / annual_opex_savings if annual_opex_savings > 0 else 0
    return {"roi_percent": round(roi, 2), "payback_years": round(payback, 2)}

TOOL_REGISTRY = {
    "run_math_calculation": run_math_calculation,
    "calculate_roi": run_math_calculation,
    "math_tool": run_math_calculation
}

# The Step 2 Validator
def validate_inputs(args):
    try:
        if float(args.get('cap_ex', 0)) <= 0:
            return False, "Capital Expenditure must be positive."
        return True, ""
    except:
        return False, "Invalid numeric data."

# The Step 3 Super Scrubber
def scrub_arguments(raw_args):
    if isinstance(raw_args, str):
        try: raw_args = ast.literal_eval(raw_args)
        except: return {}
    
    clean_dict = {}
    for k, v in raw_args.items():
        # Step 3 logic: clean the value
        cleaned_val = super_scrub(v) 
        
        # Step 1 logic: map to correct key
        key = k.lower()
        if any(x in key for x in ["cap", "cost", "exp"]): clean_dict["cap_ex"] = cleaned_val
        if any(x in key for x in ["save", "opex"]): clean_dict["annual_opex_savings"] = cleaned_val
    return clean_dict

def super_scrub(val):
    if isinstance(val, (int, float)): return float(val)
    clean_val = re.sub(r'[$,\s]', '', str(val)).lower()
    mult = 1000.0 if 'k' in clean_val else 1000000.0 if 'm' in clean_val else 1.0
    match = re.search(r"[-+]?\d*\.\d+|\d+", clean_val.replace('k','').replace('m',''))
    return float(match.group()) * mult if match else 0.0



async def main():
    agent_name = "FinOps_Analyst"
    agent = Agent(
        name=agent_name,
        instruction="Use 'run_math_calculation' for math. Then give a plain text summary.",
        model=get_model(),
        tools=[run_math_calculation]
    )

    runner = get_runner(agent)
    user_id, session_id = await initialize_session()    
    query = "Analyze a $250k project with $400,000 yearly savings."
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    stored_result = None
    
    for turn in range(1, 6):
        response_received = False
        events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
        content = None 

        async for event in events:
            if not event.content or not event.content.parts: continue

            for part in event.content.parts:
                if part.function_call:
                    call_name = part.function_call.name
                    call_id = part.function_call.id
                    
                    # Registry & Alias Check
                    target_func = TOOL_REGISTRY.get(call_name)
                    
                    if not target_func or call_name == agent_name:
                        # CIRCUIT BREAKER: If it already has math, just exit and summarize
                        if stored_result:
                            print(f"\n--- [FINAL SUMMARY] ---\nROI: {stored_result['roi_percent']}% | Payback: {stored_result['payback_years']} yrs.")
                            await cleanup(); return
                        
                        # Otherwise, tell it to try the right tool
                        res_part = types.Part(function_response=types.FunctionResponse(id=call_id, name=call_name, response={'error': 'Use math tool'}))
                        content = types.Content(role="tool", parts=[res_part]); response_received = True; break

                    # Scrub & Validate
                    clean_args = scrub_arguments(part.function_call.args)
                    valid, err = validate_inputs(clean_args)
                    
                    if not valid:
                        res_part = types.Part(function_response=types.FunctionResponse(id=call_id, name=call_name, response={'error': err}))
                        content = types.Content(role="tool", parts=[res_part]); response_received = True; break

                    # Execute
                    print(f"[TURN {turn}] Calculating...")
                    stored_result = target_func(**clean_args)
                    res_part = types.Part(function_response=types.FunctionResponse(id=call_id, name=call_name, response={'result': stored_result}))
                    content = types.Content(role="tool", parts=[res_part]); response_received = True; break

                elif part.text and part.text.strip():
                    print(f"\n--- [AGENT SUMMARY] ---\n{part.text.strip()}")
                    await cleanup(); return 

            if response_received: break
    await cleanup()

if __name__ == "__main__":
    asyncio.run(main())