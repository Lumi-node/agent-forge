# AgentForge Quick Start Guide

AgentForge provides a minimal framework for building and testing autonomous agents by separating the agent's decision-making logic from the environment it interacts with.

This guide walks you through setting up the core components: `agent.py` (the brain), `environment.py` (the world), and `main.py` (the loop).

## Prerequisites

You only need Python installed. No external libraries are required for this minimal setup.

## 1. Project Structure

Create the following file structure:

```
agentforge_project/
├── agent.py
├── environment.py
├── main.py
```

## 2. Core Modules Implementation

### `environment.py` (The World)

This module defines the simulation space—a simple 5x5 grid world.

```python
# environment.py

class SimpleGridWorld:
    """
    A simple 5x5 grid world where an agent can move and collect items.
    """
    def __init__(self, size=5):
        self.size = size
        # State: (row, col)
        self.agent_position = (0, 0)
        # Items: True if an item is present, False otherwise
        self.items = {}
        for r in range(size):
            for c in range(size):
                # Place an item randomly for demonstration
                self.items[(r, c)] = (r == 2 and c == 2)

    def get_state(self):
        """Returns the current observable state of the environment."""
        # In a real system, this would return complex observations.
        return {"position": self.agent_position, "items_present": self.items}

    def step(self, action):
        """
        Executes an action and returns the new state and reward.
        Actions: 'UP', 'DOWN', 'LEFT', 'RIGHT'
        """
        r, c = self.agent_position
        new_r, new_c = r, c

        if action == 'UP':
            new_r = max(0, r - 1)
        elif action == 'DOWN':
            new_r = min(self.size - 1, r + 1)
        elif action == 'LEFT':
            new_c = max(0, c - 1)
        elif action == 'RIGHT':
            new_c = min(self.size - 1, c + 1)

        self.agent_position = (new_r, new_c)
        reward = 0

        # Check for item collection
        if self.items.get(self.agent_position, False):
            reward = 1  # Positive reward for collecting
            self.items[self.agent_position] = False # Item is gone

        return self.get_state(), reward

    def reset(self):
        """Resets the environment to its initial state."""
        self.agent_position = (0, 0)
        # Re-initialize items for a fresh start
        self.items = {}
        for r in range(self.size):
            for c in range(self.size):
                self.items[(r, c)] = (r == 2 and c == 2)
        return self.get_state()
```

### `agent.py` (The Brain)

This module implements the `ReasoningAgent` class, which decides what to do based on observations.

```python
# agent.py

class ReasoningAgent:
    """
    An agent capable of processing observations and generating actions.
    """
    def __init__(self, name="DefaultAgent"):
        self.name = name
        self.internal_state = {}
        self.action_history = []

    def observe(self, environment_state: dict):
        """
        Updates the agent's internal knowledge based on the environment's feedback.
        """
        self.internal_state = environment_state
        print(f"[{self.name}] Observed new state: Position {environment_state['position']}")

    def think(self) -> str:
        """
        Processes the current internal state and decides the next action.
        (Simple heuristic for demonstration: move towards the center if possible)
        """
        r, c = self.internal_state['position']
        target_r, target_c = 2, 2 # Target the center of the 5x5 grid

        # Simple greedy logic: move closer to the target
        if r < target_r:
            return 'DOWN'
        elif r > target_r:
            return 'UP'
        elif c < target_c:
            return 'RIGHT'
        elif c > target_c:
            return 'LEFT'
        else:
            return 'STAY' # Should not happen in this simple loop

    def act(self, action: str) -> str:
        """
        Executes the chosen action and records it.
        Returns the action taken.
        """
        self.action_history.append(action)
        print(f"[{self.name}] Executing action: {action}")
        return action
```

### `main.py` (The Loop)

This module ties the agent and the environment together into a runnable loop.

```python
# main.py

from environment import SimpleGridWorld
from agent import ReasoningAgent

def run_simulation(agent: ReasoningAgent, environment: SimpleGridWorld, max_steps: int = 20):
    """
    Runs the main agent-environment interaction loop.
    """
    print("--- Starting Simulation ---")
    
    # 1. Initialize environment and get initial state
    current_state = environment.reset()
    
    # 2. Initialize agent with the starting state
    agent.observe(current_state)
    
    for step in range(max_steps):
        print(f"\n===== STEP {step + 1} =====")
        
        # 3. Agent Thinks (Decides action based on internal state)
        action_to_take = agent.think()
        
        # 4. Agent Acts (Executes action in the environment)
        action_executed = agent.act(action_to_take)
        
        # 5. Environment Steps (Updates world state)
        next_state, reward = environment.step(action_executed)
        
        # 6. Agent Observes (Updates internal state based on feedback)
        agent.observe(next_state)
        
        print(f"-> Environment Feedback: Reward = {reward}")

        # Termination condition (e.g., all items collected or max