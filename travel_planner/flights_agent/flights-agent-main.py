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

flights_agent = LlmAgent(
    name="FlightsAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are a flight search specialist. "
        "Given origin, destination, dates, and budget, "
        "return 2-3 realistic flight options with airline, "
        "times, layovers, and total price in JSON."
    ),
    output_key="flights",
) 

app = to_a2a(flights_agent, port=8001)