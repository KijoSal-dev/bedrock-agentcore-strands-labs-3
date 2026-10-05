# AgentCore Gateway Integration — Project Notes

 ## Project

 **Project:** WanderBot — AgentCore Gateway Integration\
 **Exercise:** Integrating APIs with AgentCore Gateway\
 **Main file:** `starter.py`

---

 # 1\. Objective

 The objective of this exercise is to connect the WanderBot travel assistant to booking-related Lambda functions through Amazon Bedrock AgentCore Gateway.

 The agent should be able to handle requests such as:

 - "Can you look up booking BK-1001?"
- "What bookings does alice@example.com have?"

 The agent should not contain the booking business logic. The booking logic remains inside the Lambda function and is accessed through AgentCore Gateway using MCP.

---

 # 2\. Architecture

 ## Intended AWS architecture

```
User
  |
  v
WanderBot (Strands Agent)
  |
  | MCP tool call
  v
AgentCore Gateway
  |
  | Lambda target
  v
Booking Lambda
  |
  v
Booking Data
```

 The agent discovers available tools from the Gateway instead of defining the booking functions locally.

---

 # 3\. Project Files

 ## `starter.py`

 Contains the WanderBot AgentCore application.

 Responsibilities:

 - Create the AgentCore application.
- Configure the Bedrock model.
- Connect to the AgentCore Gateway using `MCPClient`.
- Discover Gateway tools using `list_tools_sync()`.
- Pass the discovered tools to the Strands Agent.
- Process the user's message.

 ## `lambda/booking_lambda.py`

 Contains the booking business logic.

 The Lambda provides:

 - `get_booking(booking_ref)`
- `list_bookings_by_email(email)`

 The Lambda contains demo booking data for Alice Johnson and Bob Smith.

 ## `schema/booking_lambda.json`

 Defines the tools exposed through AgentCore Gateway.

 It contains schemas for:

 - `get_booking`
- `list_bookings_by_email`

 The Gateway uses this schema to create MCP-compatible tool definitions.

 ## `requirements.txt`

 Contains the Python dependencies required by the project.

 ## `README.md`

 Contains the original exercise instructions.

 ## `solution.py`

 Contains the provided solution/reference implementation.

 ## `local_mcp_server.py`

 A separate local MCP server created for learning and testing MCP tools with MCP Inspector.

 This file is **not part of the original AWS deployment architecture**.

 It allows the booking tools to be tested locally without deploying to AWS.

 ## `notes.md`

 Contains project documentation, commands, configuration, learning points, and recovery instructions.

---

 # 4\. MCP Integration in `starter.py`

 The following MCP classes are used:

```
from mcp.client.streamable_http import streamable_http_client
from strands.tools.mcp.mcp_client import MCPClient
```

 The Gateway client is created using:

```
client = MCPClient(
    lambda: streamable_http_client(url=GATEWAY_ENDPOINT)
)
```

 The tools are discovered using:

```
with client:
    tools = client.list_tools_sync()
```

 The discovered tools are passed to the Strands Agent:

```
agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=tools,
)
```

 The important concept is:

```
Gateway
   |
   | MCP tool definitions
   v
list_tools_sync()
   |
   v
tools
   |
   v
Agent(tools=tools)
```

 The agent therefore does not need local `@tool` definitions for the booking functions.

---

 # 5\. Gateway Tools

 The Gateway schema defines two tools.

 ## `get_booking`

 Input:

```
{
  "booking_ref": "BK-1001"
}
```

 Purpose:

 Retrieve the details of a single booking.

 Example:

```
Booking reference: BK-1001
Customer: Alice Johnson
Email: alice@example.com
Flight: HZ-101
Route: LHR → CDG
Date: 2026-03-15
Cabin: Economy Flex
Fare: $189.99
Status: CONFIRMED
```

 ## `list_bookings_by_email`

 Input:

```
{
  "email": "alice@example.com"
}
```

 Purpose:

 Retrieve all bookings associated with a customer email address.

 Alice has:

```
BK-1001
BK-1002
```

---

 # 6\. Lambda Logic

 ## Booking lookup

```
def get_booking(booking_ref: str) -> str:
    booking = BOOKINGS.get(booking_ref.upper())
    if not booking:
        return f"No booking found with reference {booking_ref}."
    return json.dumps(booking)
```

 ## Customer booking history

```
def list_bookings_by_email(email: str) -> str:
    matches = [
        b for b in BOOKINGS.values()
        if b["email"].lower() == email.lower()
    ]

    if not matches:
        return f"No bookings found for {email}."

    return json.dumps({
        "email": email,
        "bookings": matches
    })
```

---

 # 7\. Local Python Validation

 From the `Exercise` directory:

 ## Check `starter.py`

```
python -m py_compile .\starter.py
```

 No output means the syntax check passed.

 ## Check Lambda

```
python -m py_compile .\lambda\booking_lambda.py
```

 No output means the syntax check passed.

 ## Check local MCP server

```
python -m py_compile .\local_mcp_server.py
```

 No output means the syntax check passed.

 Python may create `__pycache__` directories during compilation/importing. These are normal Python bytecode cache directories and can be ignored.

---

 # 8\. MCP Inspector

 ## Purpose

 MCP Inspector is a local development and debugging tool for MCP.

 It is **not deployed to AWS**.

 It runs on the local computer and allows MCP servers and tools to be inspected.

 The Inspector was used to verify:

 - Server connection
- MCP tools
- Tool schemas
- Tool execution

---

 # 9\. How to Install/Run MCP Inspector Again

 If returning to this project later, the MCP Inspector can be started from PowerShell.

 First make sure the terminal is in the Exercise directory:

```
cd "C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M10 Integrating APIs with AgentCore Gateway\Exercise"
```

 Then run the latest Inspector:

```
npx --yes @modelcontextprotocol/inspector@latest
```

 If npm asks whether to install the package, answer:

```
y
```

 The Inspector opens in the browser.

 ### Important

 The Inspector does **not** need to be deployed.

 Do not run:

```
agentcore deploy
```

 just to use MCP Inspector.

 The Inspector is a local testing tool.

---

 # 10\. MCP Inspector Configuration

 For this project's local MCP server, use:

```
Transport Type:
STDIO
```

 Command:

```
python
```

 Arguments:

```
local_mcp_server.py
```

 Environment Variables:

```
Leave empty
```

 Authentication:

```
None
```

 Do not configure AWS authentication for the local server.

---

 # 11\. Important STDIO Rule

 When using Inspector with STDIO, **do not manually start the MCP server in another PowerShell window**.

 Do not leave this running while Inspector is trying to connect:

```
python .\local_mcp_server.py
```

 Instead, let Inspector start the process using:

```
Command:
python

Arguments:
local_mcp_server.py
```

 The Inspector launches the MCP server and communicates with it through STDIO.

---

 # 12\. If the Inspector Cannot Find `local_mcp_server.py`

 If Inspector cannot find the file, use the full path.

 Command:

```
python
```

 Arguments:

```
C:\Users\hp\Data Science and AI\AWS agentic engineer\work\Exercises\cd14763 C2 M10 Integrating APIs with AgentCore Gateway\Exercise\local_mcp_server.py
```

 Alternatively, if the Inspector provides a **Working Directory / CWD** option, set that to the Exercise folder and use:

```
local_mcp_server.py
```

---

 # 13\. What to Check in MCP Inspector

 Once connected, check the following.

 ## Server connection

 The server should show as connected.

```
wanderbot-booking-local
Connected
```

 ## Tools

 Expected tools:

```
get_booking
list_bookings_by_email
```

 ## Tool schemas

 For `get_booking`:

```
{
  "booking_ref": "BK-1001"
}
```

 For `list_bookings_by_email`:

```
{
  "email": "alice@example.com"
}
```

 ## Tool execution

 Test:

```
{
  "booking_ref": "BK-1001"
}
```

 Expected result contains:

```
Alice Johnson
BK-1001
alice@example.com
HZ-101
LHR → CDG
CONFIRMED
```

 Then test:

```
{
  "email": "alice@example.com"
}
```

 Expected result contains:

```
BK-1001
BK-1002
```

---

 # 14\. Understanding MCP Inspector

 The most important Inspector areas for this exercise are:

 1. Server connection
2. Tools
3. Tool schemas
4. Tool execution

 Resources and Prompts are MCP capabilities, but they are not the focus of this exercise.

 The important flow is:

```
MCP Server
    |
    | exposes
    v
Tools
    |
    | describe
    v
Tool Schemas
    |
    | accept
    v
Tool Arguments
    |
    | execute
    v
Tool Result
```

---

 # 15\. Local MCP Architecture

 The local testing setup is:

```
MCP Inspector
      |
      | STDIO
      v
local_mcp_server.py
      |
      +--------------------------+
      |                          |
      v                          v
get_booking             list_bookings_by_email
      |                          |
      +------------+-------------+
                   |
                   v
              Booking Data
```

 This is a local learning environment.

 No AgentCore deployment is involved.

---

 # 16\. Actual Assignment Architecture

 The actual AWS architecture is different:

```
WanderBot
    |
    | MCP
    v
AgentCore Gateway
    |
    | Lambda target
    v
booking_lambda.py
```

 The local MCP server does not replace AgentCore Gateway.

 It is only used to understand MCP concepts safely on the laptop.

---

 # 17\. Difference Between MCP Client and MCP Server

 This is an important concept from the exercise.

 ## `starter.py`

 Acts as an MCP **client**.

 It uses:

```
MCPClient
```

 and:

```
list_tools_sync()
```

 to discover tools.

 ## `local_mcp_server.py`

 Acts as an MCP **server**.

 It exposes:

```
get_booking
list_bookings_by_email
```

 to an MCP client such as MCP Inspector.

 ## AgentCore Gateway

 Acts as the MCP endpoint in the actual assignment architecture.

 Therefore:

```
Local learning:

MCP Inspector
     ↓
MCP Server
```

 while:

```
Actual exercise:

WanderBot
     ↓
MCP Client
     ↓
AgentCore Gateway
     ↓
Lambda
```

---

 # 18\. Understanding `list_tools_sync()`

 One of the most important concepts is:

```
tools = client.list_tools_sync()
```

 This asks the MCP endpoint what tools are available.

 The returned tools can then be passed directly to:

```
Agent(tools=tools)
```

 Therefore:

```
MCP endpoint
     |
     | tool definitions
     v
list_tools_sync()
     |
     v
tools
     |
     v
Strands Agent
```

 If a tool does not appear in `list_tools_sync()`, the agent cannot use that tool.

---

 # 19\. AWS Deployment Status

 The project was intentionally **not deployed to AWS** because AWS credits are limited.

 The following operations were intentionally skipped:

```
agentcore configure
agentcore deploy
agentcore invoke
```

 The Gateway endpoint remains a placeholder:

```
GATEWAY_ENDPOINT = "https://PLACEHOLDER/mcp"
```

 A real Gateway endpoint would be required for the actual AgentCore Gateway connection.

---

 # 20\. AWS Commands for Future Reference

 If AWS deployment is eventually required and credits are available, the README provides the following process.

 Install dependencies:

```
pip install -r requirements.txt
```

 Configure AgentCore:

```
agentcore configure -e starter.py -n WanderBot -dt container -rf requirements.txt --disable-memory -er $ER -ecr $ECR_URI --non-interactive
```

 Deploy:

```
agentcore deploy
```

 Test:

```
agentcore invoke '{"message": "Can you look up booking BK-1001?"}'
```

 Second test:

```
agentcore invoke '{"message": "What bookings does alice@example.com have?"}'
```

 These commands are documented here for future reference only.

 They were **not executed during this credit-saving learning session**.

---

 # 21\. What Has Been Completed

 ## Local implementation

 - [x] MCP imports added.
- [x] `MCPClient` configured.
- [x] `streamable_http_client` configured.
- [x] Gateway tool discovery implemented.
- [x] Discovered tools passed to the Strands Agent.
- [x] Lambda booking functions available.
- [x] Gateway tool schema available.
- [x] Python syntax checked.
- [x] Local MCP server created.
- [x] MCP Inspector installed.
- [x] MCP Inspector server connection tested.
- [x] MCP tools inspected.
- [x] MCP tool schemas inspected.
- [x] MCP tool execution tested successfully.

 ## AWS deployment

 - [ ] Lambda deployed.
- [ ] AgentCore Gateway created.
- [ ] Lambda registered as Gateway target.
- [ ] Gateway endpoint configured with a real URL.
- [ ] AgentCore application deployed.
- [ ] AgentCore queries invoked.

 AWS deployment and invocation were intentionally skipped to conserve AWS credits.

---

 # 22\. Key Learning

 The main lesson is that an AI agent does not need to contain the implementation of every business operation.

 Instead:

```
Agent
  |
  | discovers tools
  v
MCP / AgentCore Gateway
  |
  | routes tool call
  v
Lambda
  |
  | executes business logic
  v
Result
```

 The Gateway acts as the bridge between the AI agent and backend functionality.

 The schema tells the Gateway what tools are available and what inputs those tools require.

 `MCPClient.list_tools_sync()` allows the agent to discover those tools automatically.

 The discovered tools are then passed to:

```
Agent(tools=tools)
```

 This keeps the agent code separate from the booking business logic.

---

 # 23\. Final Project Status

```
Local implementation: COMPLETE

Local syntax validation: PASSED

Local MCP Inspector testing: COMPLETE

Server connection: PASSED

Tool discovery: PASSED

Tool schema inspection: PASSED

Tool execution: PASSED

AWS deployment: INTENTIONALLY SKIPPED

AWS invocation: INTENTIONALLY SKIPPED
```

 The local portion of the exercise is complete.

 The project can be returned to later and the MCP Inspector can be restarted using the instructions in this document.

 AWS deployment should only be performed when AWS resources/credits are available and actual AgentCore Gateway testing is required.
.