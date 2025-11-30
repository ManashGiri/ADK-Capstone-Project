import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

stays_agent = LlmAgent(
    name="StaysAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are a hotel and stay specialist. "
        "Given city, dates, budget, and preferences, "
        "return 2-3 lodging options as JSON with name, area, "
        "nightly rate, total cost, and a short rationale."
    ),
    output_key="stays",
)

app = to_a2a(stays_agent, port=8002)