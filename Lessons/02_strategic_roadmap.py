"""
LESSON 02: Strategic Roadmapping & Phased Reasoning
DESCRIPTION: Implementing a temporal reasoning framework for legacy-to-agentic transitions.
ARCHITECT'S NOTE: We are moving from 'conversational' prompting to 'structured methodology' 
instruction, ensuring the agent enforces corporate planning standards (6mo/2yr/5yr).
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model_json, get_runner, initialize_session, cleanup

import json

async def main():
    # 1. ARCHITECT DESIGN: The Principal Roadmap Specialist
    # Note the use of "Constraint-Based Instruction" to prevent generic output.
    roadmap_lead = Agent(
        name="Principal_Roadmap_Architect",
        instruction=(
            "You are a Principal Strategy Architect specializing in Digital Transformation. Output your analysis in JSON format ONLY. "
            "Your mission: Deconstruct complex legacy transitions into a three-tier roadmap: "
            "1. Tactical (6mo) | 2. Operational (2yr) | 3. Visionary (5yr). "
            "For every phase, you MUST identify: "
            "- 'Critical Dependency' (The technical prerequisite) "
            "- 'Business Outcome' (The measurable ROI/KPI)."
            "Structure: {\"roadmap\": [{\"phase\": \"...\", \"dependency\": \"...\", \"outcome\": \"...\"}]}. "
            "Do not include any text before or after the JSON."
        ),
        model=get_model_json()
    )

    # 2. ORCHESTRATION: The Runner handles the context window management
    runner = get_runner(roadmap_lead)
    
    # 3. STATE REGISTRATION: Maintaining the continuity of the CIO Suite
    user_id, session_id = await initialize_session()
    
    # 4. DATA INGESTION: The Strategic Prompt
    # We are targeting a high-friction enterprise problem: Legacy ERP migration.
    user_query = "Draft a 5-year roadmap for migrating our monolithic legacy ERP to a decentralized Agentic AI infrastructure."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- [SYSTEM] Executing Strategy Framework on Session: {session_id} ---")
    print(f"--- [LOG] Applying Phased Reasoning Methodology ---\n")
    
    # 5. EXECUTION: Asynchronous Synthesis
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- [STRATEGIC ROADMAP ARCHITECTURE] ---")
    async_response_buffer = []
    async for event in events:
        if event.is_final_response():
            output = event.content.parts[0].text
            print(output)
            async_response_buffer.append(output)
        #if event.content and event.content.parts:
        #    part_text = event.content.parts[0].text
        #    if part_text:
        #        print(part_text, end="") # See it streaming in real-time
        #        async_response_buffer.append(part_text)


    # 6. LIFECYCLE MANAGEMENT: Closing the connection to the Ollama compute node
    full_output = "".join(async_response_buffer).strip()
    try:
        # Ollama in JSON mode sometimes still adds markdown wrappers
        if full_output.startswith("```"):
            full_output = full_output.strip("`").replace("json", "", 1).strip()
        
        structured_data = json.loads(full_output)
        print("Dashboard Data Ready:", structured_data)
    except json.JSONDecodeError as e:
        print(f"Failed to parse. Raw output was: {full_output}")

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [ERROR] Architectural Failure: {e} ---")