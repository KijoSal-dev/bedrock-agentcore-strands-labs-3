 # WanderBot — Session Memory Assignment

 ## 1\. Project Purpose

 This exercise implements short-term conversation memory for WanderBot using the Strands `HookProvider` pattern and AgentCore Memory.

 The goal is for WanderBot to remember previous messages during a multi-turn conversation.

 Example:

```
Turn 1:
User: I want to plan a trip to Barcelona on a budget.

Turn 2:
User: What hotels are available under $150 per night?

Turn 3:
User: Which one has the best cancellation policy?
```

 WanderBot should remember:

 - The destination is Barcelona.
- The user has a budget preference.
- The hotels returned in the previous turn.

 Therefore, when the user says:

```
Which one has the best cancellation policy?
```

 the agent can understand that "one" refers to the previously discussed hotels.

---

 ## 2\. Cost Decision

 For this exercise, the project was tested locally instead of using the real AWS AgentCore Memory service.

 The assignment normally asks for:

```
agentcore memory create WanderBot
```

 However, AWS resources and deployment may result in charges depending on the AWS account, region, resource usage, and available credits.

 For local testing, we used:

```
MEMORY_ID = "local-test-memory"
```

 This is only a local placeholder.

 It is NOT a real AWS AgentCore Memory resource.

 We did NOT deploy the agent during the local testing.

 We also did NOT run:

```
agentcore deploy
```

---

 ## 3\. Requirements

 The project uses:

```
strands-agents
bedrock-agentcore
```

 These are stored in:

```
requirements.txt
```

 Install them with:

```
pip install -r requirements.txt
```

 This was successfully completed.

---

 ## 4\. Project Files

 The Exercise folder contains:

```
Exercise/
│
├── starter.py
├── solution.py
├── README.md
├── NOTES.md
├── requirements.txt
├── test_memory_local.py
├── memory_setup.py
│
└── datasets/
    └── hotels.json
```

 ### Important files

 ### starter.py

 This is the main assignment file.

 The `ShortTermMemoryHookProvider` is implemented here.

 ### README.md

 Contains the original assignment instructions.

 ### solution.py

 Reference/solution file supplied with the exercise.

 Do not modify it.

 ### requirements.txt

 Contains the Python dependencies.

 ### test\_memory\_local.py

 Local testing file created during this exercise.

 It uses a fake memory client so the memory functionality can be tested without making real AgentCore Memory calls.

 ### datasets/hotels.json

 Contains the hotel information used by the `search_hotels()` tool.

---

 # 5\. Step 1 — Import Hook Classes

 The assignment requires:

```
from strands.hooks import AgentInitializedEvent
from strands.hooks import HookProvider
from strands.hooks import HookRegistry
from strands.hooks import MessageAddedEvent
```

 We initially had an import problem involving `HookProvider`.

 We verified that the installed package contains `HookProvider` with:

```
python -c "from strands.hooks import HookProvider; print(HookProvider)"
```

 Successful result:

```
<class 'strands.hooks.registry.HookProvider'>
```

 We then used separate imports in `starter.py`:

```
from strands.hooks import AgentInitializedEvent
from strands.hooks import HookProvider
from strands.hooks import HookRegistry
from strands.hooks import MessageAddedEvent
```

 We verified the provider could be imported with:

```
python -c "from starter import ShortTermMemoryHookProvider; print('HookProvider import: OK')"
```

 Successful result:

```
HookProvider import: OK
```

---

 # 6\. Step 2 — Implement `__init__()`

 The `ShortTermMemoryHookProvider` constructor stores three values:

 - `memory_client`
- `memory_id`
- `last_k_turns`

 Implementation:

```
def __init__(
    self,
    memory_client: MemoryClient,
    memory_id: str,
    last_k_turns: int = 5
):
    self.memory_client = memory_client
    self.memory_id = memory_id
    self.last_k_turns = last_k_turns
```

 ### Why?

 The callbacks need access to the memory client and configuration.

 The values are later used through:

```
self.memory_client
self.memory_id
self.last_k_turns
```

 Local test result:

```
Memory provider created successfully!
Memory ID: local-test-memory
Last K turns: 5
```

---

 # 7\. Step 3 — Implement `register_hooks()`

 The provider connects lifecycle events to callback methods.

 Implementation:

```
def register_hooks(self, registry: HookRegistry) -> None:
    registry.add_callback(
        AgentInitializedEvent,
        self.on_agent_initialized,
    )

    registry.add_callback(
        MessageAddedEvent,
        self.on_message_added,
    )
```

 There are two important events.

 ## AgentInitializedEvent

 Runs when the agent is initialized.

 Purpose:

 - Retrieve previous conversation history.
- Add the history to the system prompt.

 Flow:

```
Agent initialized
        ↓
Retrieve previous memory
        ↓
Get recent turns
        ↓
Add history to system prompt
```

 ## MessageAddedEvent

 Runs when a message is added.

 Purpose:

 - Save the new message to memory.

 Flow:

```
New message
        ↓
Extract message text
        ↓
create_event()
        ↓
Save conversation
```

 Local registration test:

```
Registered callbacks:
- AgentInitializedEvent -> on_agent_initialized
- MessageAddedEvent -> on_message_added

Total callbacks: 2
```

 This test passed.

---

 # 8\. Step 4 — Understand `on_message_added()`

 The exercise provided this callback.

 It gets the actor ID:

```
actor_id = event.agent.state.get("actor_id")
```

 It gets the session ID:

```
session_id = event.agent.state.get("session_id")
```

 It extracts the message text and saves it with:

```
self.memory_client.create_event(
    memory_id=self.memory_id,
    actor_id=actor_id,
    session_id=session_id,
    messages=[(text, role.upper())],
)
```

 ### Example

 User sends:

```
I want to plan a trip to Barcelona on a budget
```

 The callback saves information associated with:

```
Actor ID: alice
Session ID: local-session-001
Role: USER
```

 Local test result:

```
[MEMORY WRITE]
Memory ID: local-test-memory
Actor ID: alice
Session ID: local-session-001
Messages: [('I want to plan a trip to Barcelona on a budget', 'USER')]
```

 This confirmed that the memory-writing callback works.

---

 # 9\. Step 5 — Understand `on_agent_initialized()`

 This callback retrieves previous conversation history.

 It gets:

```
actor_id = event.agent.state.get("actor_id")
session_id = event.agent.state.get("session_id")
```

 Then retrieves recent turns:

```
recent_turns = self.memory_client.get_last_k_turns(
    memory_id=self.memory_id,
    actor_id=actor_id,
    session_id=session_id,
    k=self.last_k_turns,
)
```

 The default is:

```
last_k_turns = 5
```

 The retrieved conversation is then added to the system prompt.

 Example:

```
Recent conversation:
User: I want to plan a trip to Barcelona on a budget
```

 This allows the agent to remember the destination and previous conversation.

---

 # 10\. Step 6 — Agent State

 The session ID and actor ID are passed into the Agent's state.

 The entry point gets the session:

```
session_id = context.session_id
```

 The actor ID comes from the payload:

```
actor_id = payload.get("actor_id", "wanderbot-user")
```

 These are passed to the Agent:

```
state={
    "session_id": session_id,
    "actor_id": actor_id,
}
```

 The hooks then access them using:

```
event.agent.state.get("session_id")
```

 and:

```
event.agent.state.get("actor_id")
```

 This connects the conversation identity to the memory system.

---

 # 11\. Session ID

 The assignment uses:

```
session_id = context.session_id
```

 The session ID is supplied by AgentCore.

 The important idea is:

```
Same session ID
        ↓
Same conversation
        ↓
Same memory context
```

 A traveller can reconnect to the same session and retain conversation context.

---

 # 12\. Actor ID

 The actor ID identifies the user.

 Example:

```
{
    "message": "I want to plan a trip to Barcelona on a budget",
    "actor_id": "alice"
}
```

 The code retrieves it using:

```
actor_id = payload.get("actor_id", "wanderbot-user")
```

---

 # 13\. Local Memory Testing

 To avoid using the real AWS Memory service, we created:

```
test_memory_local.py
```

 This file contains:

```
class FakeMemoryClient:
```

 The fake client imitates:

```
create_event()
```

 and:

```
get_last_k_turns()
```

 Instead of sending data to AWS, it stores the conversation in a Python list.

 Therefore, the memory logic can be tested locally.

---

 # 14\. Local Test — Provider Creation

 Command:

```
python test_memory_local.py
```

 Result:

```
Memory provider created successfully!
Memory ID: local-test-memory
Last K turns: 5
```

 This confirmed that `__init__()` works.

---

 # 15\. Local Test — Hook Registration

 Result:

```
Registered callbacks:
- AgentInitializedEvent -> on_agent_initialized
- MessageAddedEvent -> on_message_added

Total callbacks: 2
```

 This confirmed both callbacks were registered.

---

 # 16\. Local Test — Memory Write

 We simulated:

```
I want to plan a trip to Barcelona on a budget
```

 The fake memory client stored:

```
Memory ID: local-test-memory
Actor ID: alice
Session ID: local-session-001
Messages: [('I want to plan a trip to Barcelona on a budget', 'USER')]
```

 This proved that `on_message_added()` works.

---

 # 17\. Local Test — Memory Read

 We simulated a new agent initialization.

 The previous message was retrieved and added to the system prompt.

 Result:

```
You are WanderBot, the AI travel assistant.

Recent conversation:
User: I want to plan a trip to Barcelona on a budget
```

 This proved that `on_agent_initialized()` works.

---

 # 18\. Local Test — Three Turns

 We simulated the full conversation.

 ## Turn 1

```
I want to plan a trip to Barcelona on a budget
```

 This was stored.

 ## Turn 2

```
What hotels are available under $150 per night?
```

 When Turn 2 started, the memory contained Turn 1.

 ## Turn 3

 The memory contained:

```
Recent conversation:
User: I want to plan a trip to Barcelona on a budget
User: What hotels are available under $150 per night?
```

 This demonstrates that WanderBot has the context needed to understand:

```
Which one has the best cancellation policy?
```

 The final local test successfully stored two messages.

---

 # 19\. Python Syntax Check

 To check that `starter.py` has valid Python syntax:

```
python -m py_compile starter.py
```

 If there is no output, the syntax check passed.

 This was successfully completed.

---

 # 20\. Import Check

 To verify that the memory provider can be imported:

```
python -c "from starter import ShortTermMemoryHookProvider; print('HookProvider import: OK')"
```

 Successful result:

```
HookProvider import: OK
```

---

 # 21\. Local vs AWS Testing

 ## Local testing

 Uses:

```
FakeMemoryClient
```

 No real AgentCore Memory resource is required.

 The memory exists only in Python while the test program is running.

 ## AWS testing

 Uses:

```
MemoryClient(region_name=REGION)
```

 and a real AWS Memory ID.

 AWS deployment and service usage may incur charges.

---

 # 22\. How to Continue Working on the Project

 When returning to this project later:

 ### Step 1 — Open the Exercise folder

 Open the folder containing:

```
starter.py
README.md
requirements.txt
datasets/
```

 ### Step 2 — Install dependencies if necessary

```
pip install -r requirements.txt
```

 ### Step 3 — Check syntax

```
python -m py_compile starter.py
```

 No output means the syntax check passed.

 ### Step 4 — Check the hook import

```
python -c "from starter import ShortTermMemoryHookProvider; print('HookProvider import: OK')"
```

 Expected:

```
HookProvider import: OK
```

 ### Step 5 — Run local memory tests

```
python test_memory_local.py
```

---

 # 23\. Commands to Avoid for Local Testing

 If the goal is to continue working without creating/deploying AWS resources, do NOT run:

```
agentcore memory create WanderBot
```

 or:

```
agentcore deploy
```

 The local placeholder:

```
MEMORY_ID = "local-test-memory"
```

 is only for local testing.

 It should not be treated as a real AWS Memory ID.

---

 # 24\. AWS Deployment — Only If Required Later

 If the instructor eventually requires actual AWS deployment, the normal process is:

 ## Create Memory

```
agentcore memory create WanderBot
```

 Copy the real Memory ID.

 ## Add the real Memory ID

 Change:

```
MEMORY_ID = "local-test-memory"
```

 to:

```
MEMORY_ID = "REAL_MEMORY_ID_HERE"
```

 ## Configure the agent

 The README provides the commands for obtaining the execution role and ECR repository.

 Then:

```
agentcore configure -e starter.py -n WanderBot -dt container -rf requirements.txt -er $ER -ecr $ECR_URI
```

 ## Deploy

```
agentcore deploy
```

 Only deploy when ready to use AWS and after checking expected costs and available credits.

---

 # 25\. Final Assignment Checklist

 The assignment requires:

 - [x] Install requirements
- [x] Import `HookProvider`
- [x] Import `HookRegistry`
- [x] Import `AgentInitializedEvent`
- [x] Import `MessageAddedEvent`
- [x] Create `ShortTermMemoryHookProvider`
- [x] Implement `__init__()`
- [x] Store `memory_client`
- [x] Store `memory_id`
- [x] Store `last_k_turns`
- [x] Implement `register_hooks()`
- [x] Register `AgentInitializedEvent`
- [x] Register `MessageAddedEvent`
- [x] Use the provided `on_agent_initialized()`
- [x] Use the provided `on_message_added()`
- [x] Pass `session_id` in agent state
- [x] Pass `actor_id` in agent state
- [x] Test memory writing locally
- [x] Test memory reading locally
- [x] Test multi-turn conversation locally
- [x] Run Python syntax check
- [x] Verify hook import

---

 # 26\. The Memory Pattern to Remember

 The easiest way to remember the assignment is:

```
NEW MESSAGE
     ↓
MessageAddedEvent
     ↓
on_message_added()
     ↓
create_event()
     ↓
Memory
```

 When the agent starts again:

```
AGENT INITIALIZED
       ↓
AgentInitializedEvent
       ↓
on_agent_initialized()
       ↓
get_last_k_turns()
       ↓
Previous conversation
       ↓
system_prompt
       ↓
Agent remembers context
```

---

 # 27\. The Role of Agent State

 The state connects the hooks to the correct conversation:

```
state={
    "session_id": session_id,
    "actor_id": actor_id,
}
```

 Think of it as:

```
session_id = Which conversation?
actor_id   = Which user?
```

 Together they identify the conversation that should be read from or written to memory.

---

 # 28\. Complete Conceptual Flow

```
                  USER
                   │
                   ▼
             WanderBot Agent
                   │
                   ▼
             Agent State
          ┌────────┴────────┐
          │                 │
     session_id          actor_id
          │                 │
          └────────┬────────┘
                   ▼
              HookProvider
              /           \
             /             \
            ▼               ▼
 MessageAddedEvent    AgentInitializedEvent
            │               │
            ▼               ▼
    on_message_added  on_agent_initialized
            │               │
            ▼               ▼
     create_event()   get_last_k_turns()
            │               │
            ▼               ▼
          MEMORY          HISTORY
                            │
                            ▼
                     system_prompt
                            │
                            ▼
                         AGENT
                            │
                            ▼
                  Remembers conversation
```

---

 # 29\. What I Learned

 The main concepts learned from this exercise are:

 1. A `HookProvider` allows custom logic to run during the agent lifecycle.
2. `MessageAddedEvent` can be used to persist conversation messages.
3. `AgentInitializedEvent` can be used to retrieve previous conversation.
4. `agent.state` allows session and actor information to reach the hooks.
5. `session_id` identifies the conversation session.
6. `actor_id` identifies the user.
7. `last_k_turns` controls how much recent conversation is retrieved.
8. Previous conversation can be added to the system prompt to maintain context.
9. The memory logic can be tested locally using a fake memory client before deploying to AWS.

---

 # 30\. One-Sentence Explanation

 If asked to explain the project:

 > I implemented a Strands `HookProvider` that uses the agent's session and actor state to save messages when they are added and retrieve recent conversation history when the agent initializes, allowing WanderBot to maintain context across multiple turns.

---

 # 31\. Current Status

 ## Local Implementation

 STATUS: COMPLETE AND TESTED

```
✓ Requirements installed
✓ HookProvider available
✓ ShortTermMemoryHookProvider imports
✓ __init__() works
✓ register_hooks() works
✓ AgentInitializedEvent registered
✓ MessageAddedEvent registered
✓ Messages can be stored locally
✓ Messages can be retrieved locally
✓ Previous messages are injected into system prompt
✓ Three-turn memory scenario tested
✓ starter.py syntax checked
✓ Hook import verified
```

 ## AWS

```
Real AgentCore Memory: NOT USED FOR LOCAL TESTING
AWS deployment: NOT PERFORMED
AgentCore deployment: NOT PERFORMED
```

 This was intentional so the assignment could be learned and tested locally without unnecessary AWS usage.

---

 # 32\. Quick Restart Guide

 When I return to this assignment in the future, run these commands:

```
pip install -r requirements.txt
```

 Then:

```
python -m py_compile starter.py
```

 Then:

```
python -c "from starter import ShortTermMemoryHookProvider; print('HookProvider import: OK')"
```

 Then:

```
python test_memory_local.py
```

 If all four work, the local project is ready to continue.

---

 # END OF NOTES