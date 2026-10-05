from starter import ShortTermMemoryHookProvider


class FakeMemoryClient:
    """Local replacement for AgentCore Memory."""

    def __init__(self):
        self.events = []

    def create_event(
        self,
        memory_id,
        actor_id,
        session_id,
        messages,
    ):
        self.events.append({
            "memory_id": memory_id,
            "actor_id": actor_id,
            "session_id": session_id,
            "messages": messages,
        })

    def get_last_k_turns(
        self,
        memory_id,
        actor_id,
        session_id,
        k,
    ):
        return [
            [
                {
                    "role": role.lower(),
                    "content": {"text": text},
                }
            ]
            for event in self.events
            if event["actor_id"] == actor_id
            and event["session_id"] == session_id
            for text, role in event["messages"]
        ][-k:]


class FakeAgent:
    def __init__(self):
        self.state = {
            "session_id": "local-session-001",
            "actor_id": "alice",
        }

        self.system_prompt = (
            "You are WanderBot, the AI travel assistant."
        )


class FakeMessageEvent:
    def __init__(self, agent, message):
        self.agent = agent
        self.message = message


class FakeAgentInitializedEvent:
    def __init__(self, agent):
        self.agent = agent


# ---------------------------------------------------------
# Setup
# ---------------------------------------------------------

memory = FakeMemoryClient()

provider = ShortTermMemoryHookProvider(
    memory_client=memory,
    memory_id="local-test-memory",
    last_k_turns=5,
)


# ---------------------------------------------------------
# TURN 1
# ---------------------------------------------------------

agent = FakeAgent()

turn1 = FakeMessageEvent(
    agent,
    {
        "role": "user",
        "content": [
            {
                "text": "I want to plan a trip to Barcelona on a budget"
            }
        ],
    },
)

provider.on_message_added(turn1)

print("\n=== TURN 1 SAVED ===")


# ---------------------------------------------------------
# TURN 2
# ---------------------------------------------------------

agent = FakeAgent()

turn2 = FakeMessageEvent(
    agent,
    {
        "role": "user",
        "content": [
            {
                "text": "What hotels are available under $150 per night?"
            }
        ],
    },
)

# Load previous conversation
provider.on_agent_initialized(
    FakeAgentInitializedEvent(agent)
)

print("\n=== TURN 2 MEMORY ===")
print(agent.system_prompt)

# Save turn 2
provider.on_message_added(turn2)


# ---------------------------------------------------------
# TURN 3
# ---------------------------------------------------------

agent = FakeAgent()

# Load previous conversation again
provider.on_agent_initialized(
    FakeAgentInitializedEvent(agent)
)

print("\n=== TURN 3 MEMORY ===")
print(agent.system_prompt)

# ---------------------------------------------------------
# Final verification
# ---------------------------------------------------------

print("\n=== MEMORY CONTENTS ===")

for event in memory.events:
    print(event)

print(f"\nTotal messages stored: {len(memory.events)}")
