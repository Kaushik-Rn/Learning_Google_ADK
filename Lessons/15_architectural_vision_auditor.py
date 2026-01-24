"""
LESSON 15: Multi-Modal Intelligence (Vision-Based Auditing)
DESCRIPTION: Utilizing Vision-capable LLMs to perform technical architecture reviews.
ARCHITECT'S NOTE: Strategy isn't just prose; it's topology. By feeding raw 
architectural diagrams into our Agentic Runner, we enable 'Visual Grounding,' 
allowing the agent to spot structural risks that are invisible in text summaries.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. ARCHITECT DESIGN: The Principal Vision Specialist
    # We define a persona that understands spatial relationships and cloud topology.
    vision_lead = Agent(
        name="Principal_Architecture_Critic",
        instruction=(
            "You are a Principal Enterprise Architect. Your mission is to audit "
            "infrastructure diagrams for 2026 compliance. "
            "TASKS: 1. Inventory the core stack. 2. Highlight high-risk 'Single Points of Failure.' "
            "3. Validate alignment with 'Cloud-Native' and 'AI-Ready' standards."
        ),
        # Ensure model is set to a vision-capable variant (e.g., Llama-3.2-11b-vision)
        model=get_model() 
    )

    runner = get_runner(vision_lead)
    user_id, session_id = await initialize_session()
    
    # 2. SOURCE ASSET: The Visual Evidence
    image_path = "assets/cloud_architecture_v2.png" 
    
    print(f"--- [SYSTEM] Initializing Visual Audit | Session: {session_id} ---")
    print(f"--- [LOG] Loading Infrastructure Map: {image_path} ---\n")

    try:
        # 3. MULTI-MODAL PAYLOAD CONSTRUCTION
        # We wrap the image in a types.Part object to preserve MIME metadata.
        with open(image_path, "rb") as f:
            raw_image = f.read()

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=(
                    "Perform a pre-migration audit on this diagram. "
                    "Does this architecture support sub-second latency for AI agent orchestration?"
                )),
                types.Part(
                    inline_data=types.Blob(
                        data=raw_image,
                        mime_type="image/png"
                    )
                )
            ]
        )
        
        # 4. EXECUTION: Cross-Modal Synthesis
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        )
        
        print("--- [VISUAL ARCHITECTURAL AUDIT REPORT] ---")
        async for event in events:
            if event.is_final_response():
                print(event.content.parts[0].text)

    except FileNotFoundError:
        print(f"--- [ERROR] Asset Missing: Please ensure {image_path} exists to run Lesson 15. ---")

    # 5. LIFECYCLE MANAGEMENT
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"--- [CRITICAL] Vision Pipeline Failure: {e} ---")