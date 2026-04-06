"""Main orchestration loop for 10-step agent reasoning."""

from agent import ReasoningAgent
from environment import SimpleGridWorld


def main() -> int:
    """Execute 10-step agent reasoning loop with logging."""
    environment = SimpleGridWorld(agent_pos=(2, 2), num_items=5)
    agent = ReasoningAgent(start_position=(2, 2))

    for step_num in range(10):
        # Observe
        state = environment.get_state()
        agent.observe(state)

        # Think
        action = agent.think()

        # Log before action
        print(f"[Step {step_num}] State: {state} → Action: {action}")

        # Act
        agent.act(action, environment)

        # Log after action
        new_state = environment.get_state()
        print(f"[Step {step_num}] New State: {new_state}")

    # Final message
    print("✓ Agent completed 10 steps successfully.")
    return 0


if __name__ == "__main__":
    exit(main())
