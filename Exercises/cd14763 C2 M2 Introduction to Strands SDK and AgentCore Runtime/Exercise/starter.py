"""
================================================================================
WanderBot — EXERCISE: Strands SDK + AgentCore Runtime
================================================================================
Your first WanderBot. Wire up a Strands Agent with the built-in calculator
tool inside a BedrockAgentCoreApp, then deploy it to AgentCore Runtime.

STEPS
-----
  Step 1: Import BedrockAgentCoreApp, Agent, BedrockModel, calculator
  Step 2: Create the BedrockAgentCoreApp instance
  Step 3: Configure BedrockModel with MODEL_ID
  Step 4: Write a SYSTEM_PROMPT that defines WanderBot's persona
  Step 5: Inside invoke(), build an Agent(model, system_prompt, tools=[calculator])
          and return agent(user_message)
"""

import logging

# TODO (Step 1): Import BedrockAgentCoreApp from bedrock_agentcore.runtime
# TODO (Step 1): Import Agent from strands
# TODO (Step 1): Import BedrockModel from strands.models
# TODO (Step 1): Import calculator from strands_tools

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("WanderBot.AgentCoreRuntime")

# ---------------------------------------------------------------------------
# AgentCore app instance
# ---------------------------------------------------------------------------
# TODO (Step 2): Create the BedrockAgentCoreApp instance
# app = ...
app = BedrockAgentCoreApp()

# ---------------------------------------------------------------------------
# Foundation model — Amazon Nova 2 Lite via a cross-region inference profile.
# Optional tuning: temperature=0.1, max_tokens=1024
# ---------------------------------------------------------------------------
MODEL_ID = "us.amazon.nova-2-lite-v1:0"

# TODO (Step 3): Configure the BedrockModel with MODEL_ID
# model = ...
model = BedrockModel(
    model_id=MODEL_ID,
    temperature=0.1,
    max_tokens=1024,
)

# ---------------------------------------------------------------------------
# WanderBot system prompt
# ---------------------------------------------------------------------------
# TODO (Step 4): Write a SYSTEM_PROMPT string that describes:
#   - WanderBot's role as Horizon Travel's AI assistant
#   - Horizon Travel's services (flights, hotels, insurance, loyalty programme)
#   - When to use the calculator tool
#   - Style guidelines (friendly, concise)
SYSTEM_PROMPT = """
You are WanderBot, Horizon Travel's AI assistant.
You help customers with flights, hotels, travel insurance, baggage, check-in, cabin classes, cancellation policies, and the loyalty programme.
You must use the calculator tool for all numeric calculations, and you must not do calculations yourself.
The communication style should be friendly, concise, and professional.
"""

# ---------------------------------------------------------------------------
# Agent entry point — called for every incoming request
# ---------------------------------------------------------------------------
# TODO (Step 5): Decorate this function with @app.entrypoint
@app.entrypoint
async def invoke(payload: dict, context=None):
    """WanderBot — Agent entry point."""
    user_message = payload.get("message", "Hello!")
    logger.info("User: %s", user_message[:80])

    # TODO (Step 5): Build the Agent and return its response
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[calculator])

    response = agent(user_message)
    return response


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
