# AgentForge API Reference

AgentForge is a minimal framework designed to build and test autonomous agents by separating the agent's reasoning logic from the environment simulation.

---

## 🐍 `agent.py`

This module contains the core logic for the intelligent agent, responsible for perceiving the environment, deciding on actions, and executing them.

### `ReasoningAgent` Class

The central class representing the agent's decision-making entity.

**Signature:**
```python
class ReasoningAgent:
    def __init__(self, initial_state: dict):
        # Initializes the agent with a starting state representation
        pass

    def think(self, state: dict) -> str:
        """
        Processes the current state provided by the environment and determines the next action.

        Args:
            state (dict): A dictionary representing the current observation from the environment.

        Returns:
            str: The action command to be executed (e.g., "NORTH", "MOVE").
        """
        # Implementation handles state parsing and policy execution
        pass

    def act(self, action: str) -> None:
        """
        Executes the given action within the environment context.
        (Note: In this minimal framework, this might just pass the action to the environment handler).

        Args:
            action (str): The action determined by the agent's 'think' method.
        """
        pass

    def observe(self, feedback: dict) -> None:
        """
        Updates the agent's internal state based on feedback received from the environment after an action.

        Args:
            feedback (dict): A dictionary containing observations like new position, rewards, etc.
        """
        pass
```

**Example Usage:**
```python
from agent import ReasoningAgent

# Initialize the agent
agent = ReasoningAgent(initial_state={"position": (0, 0), "goal_found": False})

# Simulate a decision cycle
current_state = {"position": (1, 1), "nearby_items": ["key"]}
next_action = agent.think(current_state)  # Returns "NORTH"

# Execute the action (handled by the main loop/environment)
# agent.act(next_action)

# Receive feedback after action
environment_feedback = {"new_position": (1, 2), "reward": 1}
agent.observe(environment_feedback)
```

---

## 🌍 `environment.py`

This module defines the simulated world in which the agent operates.

### `SimpleGridWorld` Class

Represents a discrete, bounded 5x5 grid environment.

**Signature:**
```python
class SimpleGridWorld:
    def __init__(self, size: int = 5):
        """
        Initializes the grid world.

        Args:
            size (int): The dimension of the square grid (e.g., 5 for 5x5).
        """
        pass

    def get_initial_state(self) -> dict:
        """
        Returns the starting state representation for the agent.

        Returns:
            dict: The initial state dictionary.
        """
        pass

    def step(self, action: str, current_state: dict) -> tuple[dict, dict]:
        """
        Executes an action in the environment and calculates the resulting state and feedback.

        Args:
            action (str): The action taken by the agent (e.g., "NORTH", "SOUTH").
            current_state (dict): The agent's current state.

        Returns:
            tuple[dict, dict]: A tuple containing (new_state, feedback).
        """
        # Handles boundary checks and state transitions
        pass
```

**Example Usage:**
```python
from environment import SimpleGridWorld

# Initialize the environment
world = SimpleGridWorld(size=5)

# Get the starting point
initial_state = world.get_initial_state()
print(f"Starting State: {initial_state}")

# Simulate an action (assuming the agent decided to move NORTH)
action_to_take = "NORTH"
new_state, feedback = world.step(action_to_take, initial_state)

print(f"New State: {new_state}")
print(f"Feedback Received: {feedback}")
```

---

## 🚀 `main.py`

This module serves as the entry point and orchestrator, managing the interaction loop between the agent and the environment.

### `run_simulation` Function

The primary function that executes the agent-environment interaction loop.

**Signature:**
```python
def run_simulation(agent: ReasoningAgent, environment: SimpleGridWorld, max_steps: int = 100) -> None:
    """
    Runs the main agent-environment interaction loop.

    Args:
        agent (ReasoningAgent): The agent instance to control.
        environment (SimpleGridWorld): The environment instance to interact with.
        max_steps (int): The maximum number of steps the simulation should run for.
    """
    # Manages the loop: Observe -> Think -> Act -> Observe
    pass
```

**Example Usage:**
```python
from agent import ReasoningAgent
from environment import SimpleGridWorld
from main import run_simulation

# 1. Setup
env = SimpleGridWorld()
agent = ReasoningAgent(env.get_initial_state())

# 2. Run the simulation
print("--- Starting AgentForge Simulation ---")
run_simulation(agent, env, max_steps=50)
print("--- Simulation Finished ---")
```