# Lab: Building Foundry Agents with Python

## Overview
In this hands-on lab, you will learn how to create intelligent AI agents using Microsoft Foundry, both through the portal and programmatically using Python. You'll create agents with tools like Web Search and Code Interpreter, and immediately use them through Python code. This lab demonstrates a streamlined approach to building production-ready AI agents.

**Prerequisites:**
- An Azure account with an active subscription
- Basic understanding of AI agents and Python programming
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python 3.9+](https://www.python.org/downloads/) installed and on your `PATH`

---

## Lab Architecture
By the end of this lab, you will have:
- A Microsoft Foundry resource with a deployed project
- A GPT model deployment for agent responses
- An AI agent created in the Foundry Portal with custom instructions
- Python code that creates a multi-tool agent (web search + code interpreter) and demonstrates both capabilities

---

## Step 1: Setup a Foundry Project

### 1.1 Access Microsoft Foundry Portal
1. **Go to Foundry Portal** by navigating to [https://ai.azure.com/](https://ai.azure.com/)
2. Sign in with your Azure credentials
3. Verify that you are in the **New** Foundry Portal and that your project (`python-agents-project`) is selected in the upper left corner
> Note: If you are in the Old Foundry Portal, you may need to switch to the New Portal using the toggle at the top of the page

### 1.2 Deploy a Model for Your Agent
1. In Microsoft Foundry, navigate to **Build** in the top navigation
2. Select **Models** from the left sidebar
3. Click **Deploy a base model**
4. Search for the **gpt-5.4** model
5. **Select** the model
6. Select **Deploy** > **Custom settings**
7. Configure the deployment:
   - **Deployment name:** `gpt-5.4`
   - **Deployment type:** Select **Global Standard** (pay-per-token, easiest for testing)
   - **Tokens per minute rate limit:** `50000`
8. Click **Deploy**
9. Wait for deployment to complete (typically 1-3 minutes)

### 1.3 Verify Model Deployment
1. Once deployment completes, you should be sent to the Playground with the `gpt-5.4` model selected
2. In the input box, enter a test prompt:
   ```
   What is Microsoft Foundry?
   ```
3. Click **Submit**
4. Verify you receive a coherent response describing Microsoft Foundry

---

## Step 2: Create an AI Agent in Foundry Portal

### 2.1 Navigate to Agent Builder
1. In Microsoft Foundry Portal, navigate to **Build** > **Agents** in the left sidebar
2. Click **Create agent**

### 2.2 Configure Agent Basics
1. On the **Create an agent** page:
   - **Agent name:** `pythonassistant`
2. Click **Create and open playground**

### 2.3 Configure Agent Instructions
1. In the agent configuration page, navigate to the **Instructions** tab
2. In the **Instructions** field, add detailed instructions:
   ```
   You are a helpful AI assistant specializing in Python programming and general knowledge.

   Guidelines:
   - Provide clear, concise, and accurate answers
   - When asked about current events or web information, use web search
   - When asked to write or execute code, use the code interpreter tool
   - Maintain a professional and friendly tone
   - If a question is ambiguous, ask for clarification
   - Explain your reasoning when appropriate

   When providing answers:
   1. Use web search for current information and real-time data
   2. Use code interpreter for calculations, data analysis, or code execution
   3. Provide clear, actionable answers
   4. Cite sources when using web search
   ```

### 2.4 Verify Tools
1. Navigate to the **Tools** section of the agent configuration
2. Verify that **Web search** is available. Web search should be enabled by default for new agents. If not, click **Add** and enable Web search.
3. Click **Add** to enable the **Code interpreter** tool.
4. Verify that both tools are listed under the agent's tools.

### 2.5 Save Your Agent
1. Click **Save** in the upper right corner

---

## Step 3: Test Your Agent in the Playground

### 3.1 Verify Agent Setup
1. In your agent configuration, you'll see a chat interface on the right side
2. Start with a greeting:
   ```
   Hello! Can you tell me what you can help me with?
   ```
3. Verify the agent responds appropriately and describes its capabilities

### 3.2 Test Web Search
1. Ask a question that requires current information:
   ```
   What are the latest developments in AI technology this week?
   ```
2. Verify the response:
   - ✅ Agent performs a web search
   - ✅ Agent provides current information
   - ✅ Agent cites sources

### 3.3 Test Code Interpreter
1. Ask a question that requires code execution:
   ```
   Calculate the factorial of 10 and show me the Python code
   ```
2. Verify the agent executes code and provides the result

### 3.4 Review Agent Logs
1. Click on the **Logs** at the bottom
2. Review the tool calls performed (web search and code interpreter)

---

## Step 4: Setup Your Local Development Environment in VS Code

### 4.1 Open VS Code and a Terminal
1. Launch **Visual Studio Code**
2. Select **File** > **Open Folder...** and choose (or create) a folder for this lab
3. Open the integrated terminal with **Terminal** > **New Terminal** (or press `` Ctrl+` ``)
4. On Windows, the terminal opens in **PowerShell** by default, which the commands below assume

> **Note:** VS Code's integrated terminal gives you the `code` command for editing files and a full-featured editor, so you can create, run, and debug your Python scripts all in one place.

### 4.2 Create a Working Directory
1. In the terminal, create a new directory for your Python scripts and change into it:
   ```powershell
   mkdir foundry-agents-lab
   cd foundry-agents-lab
   ```

### 4.3 Create a Virtual Environment
1. Create a Python virtual environment:
   ```powershell
   python -m venv agentenv
   ```
2. Activate the virtual environment:
   ```powershell
   .\agentenv\Scripts\Activate.ps1
   ```
   > **macOS/Linux (or Git Bash/WSL):** use `source agentenv/bin/activate` instead.
   > If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` and try again.
3. Verify the virtual environment is activated (you should see `(agentenv)` in your prompt)

**Why use a virtual environment?**
- ✅ Isolates project dependencies
- ✅ Prevents package conflicts
- ✅ Makes your environment reproducible
- ✅ Allows different Python package versions per project

> **Tip:** Press `Ctrl+Shift+P`, run **Python: Select Interpreter**, and choose the `agentenv` environment so VS Code uses it when running and debugging your scripts.

### 4.4 Install Required Packages
1. Install the Azure AI Projects SDK (with virtual environment activated):
   ```powershell
   pip install "azure-ai-projects==2.1.0"
   pip install azure-identity
   pip install openai
   pip install python-dotenv
   ```

### 4.5 Get Your Project Endpoint
1. In the Foundry Portal, select Home from the top navigation bar.
2. Locate and copy the **Project Endpoint**
   - Format: `https://foundry-python-<yourname>.services.ai.azure.com/api/projects/python-agents-project`
3. Save this endpoint for use in your Python code

### 4.6 Create your Environment File
1. In the terminal, create and open a new file to store environment variables:
   ```powershell
   code .env
   ```
2. Add the following to the `.env` file, replacing the URL with your actual project endpoint:
   ```
   PROJECT_ENDPOINT="https://foundry-python-<yourname>.services.ai.azure.com/api/projects/python-agents-project"
   ```
3. Save the file with `Ctrl+S`

### 4.7 Login to Azure
1. In the terminal, run the following command to login:
   ```powershell
   az login
   ```
2. Follow the instructions to complete the login process (a browser window opens for you to sign in)
3. Once logged in, select the correct subscription in the terminal then press Enter.

---

## Step 5: Create and Use an Agent Programmatically with Python

In this step, you'll learn how to create and use a conversation with your agent programmatically using Python.

### 5.1 Create and Use a Conversation
1. In VS Code, create a new Python file:
   ```powershell
   code conversation_agent.py
   ```
2. Add the following code:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition, 
    WebSearchTool, 
    CodeInterpreterTool
)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get project endpoint from environment
PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("MODEL_DEPLOYMENT")

# Create project client
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

print("=" * 60)
print("STEP 1: CREATE AN AGENT WITH TOOLS")
print("=" * 60)

# Step 1: Create an agent with multiple tools
agent = project.agents.create_version(
    agent_name="python-multitool-agent",
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT,
        instructions="""You are a versatile AI assistant with multiple capabilities:
        - Use web search for current information and real-time data
        - Use code interpreter for calculations, data analysis, and code execution
        - Provide clear and accurate answers
        - Cite sources when using web search""",
        tools=[WebSearchTool(), CodeInterpreterTool()],
    ),
)

print(f"✅ Agent created successfully!")
print(f"Agent Name: {agent.name}")
print(f"Agent Version: {agent.version}")
print(f"Tools: Web Search, Code Interpreter\n")


# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

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
            "name": agent.name,
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
            "name": agent.name,
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
            "name": agent.name,
            "type": "agent_reference",
        }
    },
    input="Calculate the population density if the city area is 105 square kilometers.",
)
print(f"Status: {calculation.status}")
print(f"User: Calculate the population density if the city area is 105 square kilometers.")
print(f"Assistant: {calculation.output_text}")
print("=" * 60)
```
> Note: You may copy the code from the agent.py file found in the Agents-Python folder if you want to skip typing it out manually.
3. Save the file with `Ctrl+S`
4. Run the script (it creates the multi-tool agent for you):
   ```powershell
   python agent.py
   ```
---

## Step 6: Call Published Agent via OpenAI SDK

### 6.1 Publish Your Agent
1. In the Foundry Portal, select **Build**.
2. Select **Agents** and navigate to your agent (`python-multitool-agent`)
3. Select **Publish** in the upper right.
4. Copy the **Endpoint (Responses)** endpoint URL
   - Format: `https://foundry-python-<yourname>.services.ai.azure.com/api/projects/python-agents-project/agents/python-multitool-agent/endpoint/protocols/openai/v1/responses`
5. Update your `.env` file to add the BASE_URL:
   ```powershell
   code .env
   ```
6. Add this line to your `.env` file with your actual endpoint:
   ```
   BASE_URL="https://foundry-python-<yourname>.services.ai.azure.com/api/projects/python-agents-project/agents/python-multitool-agent/endpoint/protocols/openai"
   ```
   > **Important:** The `BASE_URL` should stop before `/v1/responses` because the OpenAI SDK will append that path internally when making requests.
7. Save with `Ctrl+S`

### 6.2 Call Published Agent (Streaming)
1. In VS Code, create a new Python file:
   ```powershell
   code call_published_agent.py
   ```
2. Add the following code:

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if needed

# 1) Get Entra ID token (same audience as az account get-access-token --resource https://ai.azure.com)
credential = DefaultAzureCredential()
token = credential.get_token("https://ai.azure.com/.default")  
BASE_URL = os.getenv("BASE_URL") 
# 2) IMPORTANT: base_url must stop BEFORE "/v1/responses"
#    Because the SDK will call POST {base_url}/v1/responses internally.

client = OpenAI(
    api_key=token.token,  # sent as "Authorization: Bearer <token>"
    base_url=BASE_URL,
    default_query={"api-version": "2025-11-15-preview"},
    default_headers={"Foundry-Features": "AgentEndpoints=V1Preview"},
)

# 3) Invoke the agent
stream = client.responses.create(
    input="Give me 5 benefits of Microsoft Foundry in bullet points.",
    stream=True
)


print("\n" + "=" * 60)
print("CALLING PUBLISHED AGENT:")
print("=" * 60)

# Should iterate through streaming events and print the response as it comes in
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()  # newline at end

```
> Note: You may copy the code from the call_published_agent.py file found in the Agents-Python folder if you want to skip typing it out manually.
3. Save the file with `Ctrl+S`
4. Run the script:
   ```powershell
   python call_published_agent.py
   ```

### 6.3 Calling the Published Agent via cURL
You can also call the published agent using cURL from the VS Code terminal. The commands below use **PowerShell** (the default VS Code terminal on Windows).
1. First, get an access token using Azure CLI:
```powershell
$TOKEN = az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
$TOKEN.Length   # should print a non-zero length
```
> Note: You must be logged in to Azure CLI (via az login) and have the appropriate permissions (Azure AI User) to get an access token. The token will be used for authentication when calling the published agent.
2. Use the following cURL command to call the published agent, replacing `<BASE_URL>` with your actual values:
```powershell
curl.exe -i --fail-with-body -X POST `
"<BASE_URL>/responses?api-version=2025-11-15-preview" `
  -H "Authorization: Bearer $TOKEN" `
  -H "Content-Type: application/json" `
  -H "Foundry-Features: AgentEndpoints=V1Preview" `
  -d '{"input": "What are the benefits of using Microsoft Foundry?"}'
```
> Note: Remove `/v1/responses` from the BASE_URL when using it in the cURL command, as the path is included in the command itself.
> **macOS/Linux (or Git Bash/WSL):** use `curl` instead of `curl.exe`, replace the backtick (`` ` ``) line-continuations with `\`, and set the token with `TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)`.

Sample:
```powershell
curl.exe -i --fail-with-body -X POST `
"https://foundry-python-ziggy.services.ai.azure.com/api/projects/python-agents-project/agents/python-multitool-agent/endpoint/protocols/openai/responses?api-version=2025-11-15-preview" `
  -H "Authorization: Bearer $TOKEN" `
  -H "Content-Type: application/json" `
  -H "Foundry-Features: AgentEndpoints=V1Preview" `
  -d '{"input":"What are the benefits of using Microsoft Foundry?"}'
```  
3. You should receive a response from the agent with a full JSON payload containing the agent's answer to the question.

### 6.4 Understanding Published Agents
Published agents expose an OpenAI-compatible API endpoint that:
- ✅ Requires Azure RBAC authentication (Azure AI User role)
- ✅ Requires client-side conversation history management
- ✅ Can be consumed from any application with proper credentials
- ✅ Provides a managed, scalable API endpoint

> **Note:** Published agents are ideal for production scenarios where you need a managed API endpoint without maintaining server infrastructure.

---

## Summary and Key Takeaways

In this lab, you successfully:

1. ✅ Created a Foundry resource and deployed a GPT model
2. ✅ Created an AI agent in the Foundry Portal with custom instructions
3. ✅ Tested the agent with web search and code interpreter tools
4. ✅ Set up a local Python environment in VS Code with required Azure SDK packages
5. ✅ **Mastered the 5-step agent workflow pattern:**
   - Step 1: Create an agent
   - Step 2: Create a conversation (optional)
   - Step 3: Generate a response
   - Step 4: Check response status
   - Step 5: Retrieve the response
6. ✅ Created and used agents programmatically with Python
7. ✅ Demonstrated both context management approaches (`previous_response_id` and `conversations`)
8. ✅ Created multi-tool agents with Web Search and Code Interpreter
9. ✅ Monitored tool execution status and inspected outputs
10. ✅ Implemented streaming responses with status monitoring
11. ✅ Published agent and consumed it via OpenAI SDK

### Key Concepts

**Agent Runtime Workflow:**
- **Step 1**: Create agents with instructions and tools
- **Step 2**: Use conversations for context
- **Steps 3-5**: Generate → Check Status → Retrieve pattern for all interactions
- **Streaming**: Monitor event types and status throughout the stream

**Agent Creation Patterns:**
- **Portal-based:** Quick visual creation with UI configuration
- **SDK-based:** Programmatic creation with version control and automation
- **Published:** Managed API endpoints for production consumption

**Tool Integration:**
- **Web Search:** Enables agents to access current information
- **Code Interpreter:** Enables agents to execute Python code
- **Multi-tool:** Agents can use multiple tools based on context

**Response Patterns:**
- **Synchronous:** Wait for complete response before continuing
- **Streaming:** Receive partial results in real-time
- **Background:** Long-running tasks executed asynchronously

### Best Practices

1. **Authentication:** `DefaultAzureCredential()` automatically uses your `az login` credentials from the terminal
2. **Tool Selection:** Choose tools based on agent purpose (web search for current info, code interpreter for calculations)
3. **Streaming:** Use streaming for better user experience with long responses
4. **Conversations:** Use conversations for multi-turn context when server-side storage is acceptable
5. **Published Agents:** Use for production APIs with RBAC security
6. **VS Code:** Use the built-in `code` command and integrated terminal to create, edit, run, and debug your scripts in one place

---

**End of Lab**
