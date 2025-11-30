import json
import requests
import subprocess
import time
import uuid
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from google.adk.agents import LlmAgent , ParallelAgent, SequentialAgent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Hide additional warnings in the notebook
import warnings

warnings.filterwarnings("ignore")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

flights_process = subprocess.Popen(
    [
        "uvicorn",
        "flights-agent-main:app",  # Module:app format
        "--host",
        "localhost",
        "--port",
        "8001",
    ],
    cwd="travel_planner/flights_agent",  # Run from /tmp where the file is
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, 
)

stays_process = subprocess.Popen(
    [
        "uvicorn",
        "stays-agent-main:app",  # Module:app format
        "--host",
        "localhost",
        "--port",
        "8002",
    ],
    cwd="travel_planner/stays_agent",  # Run from /tmp where the file is
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, 
)

activities_process = subprocess.Popen(
    [
        "uvicorn",
        "activities-agent-main:app",  # Module:app format
        "--host",
        "localhost",
        "--port",
        "8003",
    ],
    cwd="travel_planner/activities_agent",  # Run from /tmp where the file is
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, 
)



# max_attempts = 30
# for attempt in range(max_attempts):
#     try:
#         response = requests.get(
#             "http://localhost:8001/.well-known/agent-card.json", timeout=1
#         )
#         if response.status_code == 200:
#             print(f"\n✅ Product Catalog Agent server is running!")
#             print(f"   Server URL: http://localhost:8001")
#             print(f"   Agent card: http://localhost:8001/.well-known/agent-card.json")
#             break
#     except requests.exceptions.RequestException:
#         time.sleep(5)
#         print(".", end="", flush=True)
# else:
#     print("\n⚠️  Server may not be ready yet. Check manually if needed.")

# # Store the process so we can stop it later
# globals()["product_catalog_server_process"] = server_process

# # Fetch the agent card from the running server
# try:
#     response = requests.get(
#         "http://localhost:8001/.well-known/agent-card.json", timeout=5
#     )

#     if response.status_code == 200:
#         agent_card = response.json()
#         print("📋 Product Catalog Agent Card:")
#         print(json.dumps(agent_card, indent=2))

#         print("\n✨ Key Information:")
#         print(f"   Name: {agent_card.get('name')}")
#         print(f"   Description: {agent_card.get('description')}")
#         print(f"   URL: {agent_card.get('url')}")
#         print(f"   Skills: {len(agent_card.get('skills', []))} capabilities exposed")
#     else:
#         print(f"❌ Failed to fetch agent card: {response.status_code}")

# except requests.exceptions.RequestException as e:
#     print(f"❌ Error fetching agent card: {e}")
#     print("   Make sure the Product Catalog Agent server is running (previous cell)")

flights_remote_agent = RemoteA2aAgent(
    name="flights_remote_agent",
    description="Call the FlightsAgent to get flight options.",
    # Point to the agent card URL - this is where the A2A protocol metadata lives
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

stays_remote_agent = RemoteA2aAgent(
    name="stays_remote_agent",
    description="Call the StaysAgent to get stay options.",
    # Point to the agent card URL - this is where the A2A protocol metadata lives
    agent_card=f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}",
)
activities_remote_agent = RemoteA2aAgent(
    name="activities_remote_agent",
    description="Call the ActivitiesAgent to get activity suggestions.",
    # Point to the agent card URL - this is where the A2A protocol metadata lives
    agent_card=f"http://localhost:8003{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Wrapper agents that use the tools and write to shared state
flights_wrapper = LlmAgent(
    name="FlightsWrapper",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are orchestrating a call to the FlightsAgent via an A2A sub agent. "
        "Use the sub agent to fetch flights and save them under state['flights'] "
        "without reformatting too much."
    ),
    sub_agents=[flights_remote_agent],
    output_key="flights",
)

stays_wrapper = LlmAgent(
    name="StaysWrapper",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are orchestrating a call to the StaysAgent via an A2A sub agent. "
        "Use the sub agent to fetch stays and save them under state['stays']."
    ),
    sub_agents=[stays_remote_agent],
    output_key="stays",
)

activities_wrapper = LlmAgent(
    name="ActivitiesWrapper",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "You are orchestrating a call to the ActivitiesAgent via an A2A sub agent. "
        "Use the sub agent to fetch activities and save them under state['activities']."
    ),
    sub_agents=[activities_remote_agent],
    output_key="activities",
)

# Parallel research step
research_parallel = ParallelAgent(
    name="ResearchParallel",
    sub_agents=[flights_wrapper, stays_wrapper, activities_wrapper],
)

synthesis_agent = LlmAgent(
    name="TripSynthesizer",
    model=Gemini(model="gemini-2.5-pro", retry_options=retry_config),
    instruction=(
        "You are a senior travel planner. You receive state that already "
        "contains 'flights', 'stays', and 'activities'. "
        "1) Build 1-2 complete itineraries (day-by-day) that fit budget. "
        "2) Explain pros/cons of each option. "
        "3) Output clean JSON with keys: options, recommended_option, summary."
        "Don't display raw JSON, convert to user-friendly text."
    ),
    output_key="trip_plan",
)

# Full workflow: TripPlanner root agent
trip_planner_workflow = SequentialAgent(
    name="TripPlannerWorkflow",
    sub_agents=[
        research_parallel,   # gather info in parallel
        synthesis_agent,     # combine into plan
    ],
)

root_agent = trip_planner_workflow
