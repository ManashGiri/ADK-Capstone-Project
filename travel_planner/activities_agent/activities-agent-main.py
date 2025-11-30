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

activities_agent = LlmAgent(
    name="ActivitiesAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are a local activities planner. "
        "Given destination, dates, interests, and budget, "
        "return 4-6 activities in JSON grouped by day, "
        "with time of day and short descriptions."
    ),
    output_key="activities",
)

app = to_a2a(activities_agent, port=8003)