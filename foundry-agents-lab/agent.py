from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition, 
    WebSearchTool, 
    CodeInterpreterTool,
    AutoCodeInterpreterToolParam,
)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get project endpoint from environment
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
AGENT_NAME = "python-multitool-agent"

# Create project client
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Upload Sales.xlsx for the code interpreter to use
sales_path = os.path.join(os.path.dirname(__file__), "..", "Sales.xlsx")
with open(sales_path, "rb") as sales_file:
    uploaded_file = project.get_openai_client().files.create(
        purpose="assistants", file=sales_file
    )
print(f"✅ Uploaded Sales.xlsx (file ID: {uploaded_file.id})\n")

print("=" * 60)
print("STEP 1: CREATE AN AGENT WITH TOOLS")
print("=" * 60)

# Step 1: Create an agent with multiple tools
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions="""You are a versatile AI assistant with multiple capabilities:
        - Use web search for current information and real-time data
        - Use code interpreter for calculations, data analysis, and code execution
        - Provide clear and accurate answers
        - Cite sources when using web search""",
        tools=[
            WebSearchTool(),
            CodeInterpreterTool(
                container=AutoCodeInterpreterToolParam(file_ids=[uploaded_file.id])
            ),
        ],
    ),
)

print(f"✅ Agent created successfully!")
print(f"Agent Name: {AGENT_NAME}")
print(f"Agent Version: {agent.version}")
print(f"Tools: Web Search, Code Interpreter\n")


# Get an OpenAI client pre-bound to the specified agent
openai = project.get_openai_client(agent_name=AGENT_NAME)


print("=" * 60)
print("STEP 2: CREATE A CONVERSATION")
print("=" * 60)

# Step 2: Create a conversation for multi-turn chat
conversation = openai.conversations.create()
print(f"✅ Conversation created with ID: {conversation.id}")
print("This maintains history across all turns automatically.\n")

# First turn
print("=" * 60)
print("STEP 3-5: TURN 1 (Generate & Retrieve)")
print("=" * 60)
response = openai.responses.create(
    conversation=conversation.id,  # Pass conversation ID
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input="What is the capital of France?",
)
print(f"Status: {response.status}")
print(f"User: What is the capital of France?")
print(f"Assistant: {response.output_text}\n")

# Follow-up turn in the same conversation
print("=" * 60)
print("STEP 3-5: TURN 2 (Generate & Retrieve)")
print("=" * 60)
follow_up = openai.responses.create(
    conversation=conversation.id,  # Same conversation ID maintains context
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input="What is the population of that city?",
)
print(f"Status: {follow_up.status}")
print(f"User: What is the population of that city?")
print(f"Assistant: {follow_up.output_text}\n")

# Third turn with a calculation request
print("=" * 60)
print("STEP 3-5: TURN 3 (Generate & Retrieve - with tool use)")
print("=" * 60)
calculation = openai.responses.create(
    conversation=conversation.id,  # Context from all previous turns
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input="Calculate the population density if the city area is 105 square kilometers.",
)
print(f"Status: {calculation.status}")
print(f"User: Calculate the population density if the city area is 105 square kilometers.")
print(f"Assistant: {calculation.output_text}\n")

# Fourth turn: analyze the uploaded Sales.xlsx file
print("=" * 60)
print("STEP 3-5: TURN 4 (Generate & Retrieve - Sales file insights)")
print("=" * 60)
sales_prompt = (
    "Using the uploaded Sales.xlsx file, analyze the data with code interpreter "
    "and give me key insights: total sales, top-performing categories, and any "
    "notable trends."
)
sales_insights = openai.responses.create(
    conversation=conversation.id,  # Context from all previous turns
    extra_body={
        "agent_reference": {
            "name": AGENT_NAME,
            "type": "agent_reference",
        }
    },
    input=sales_prompt,
)
print(f"Status: {sales_insights.status}")
print(f"User: {sales_prompt}")
print(f"Assistant: {sales_insights.output_text}")
print("=" * 60)