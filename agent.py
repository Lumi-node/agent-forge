"""ReasoningAgent: Implements the think-act-observe cycle for autonomous reasoning."""


class ReasoningAgent:
    """Agent that reasons about environment and takes actions."""

    def __init__(self, start_position=(2, 2)):
        """Initialize agent position, observations, and action history."""
        self.position = start_position
        self.observations = {}
        self.action_history = []

    def think(self):
        """Decide next action based on observations (deterministic heuristic)."""
        grid = self.observations.get("grid")
        items_remaining = self.observations.get("items_remaining", 0)

        agent_row, agent_col = self.position

        # Step 1: Check if item at current position
        if grid[agent_row][agent_col] == 1:
            return "collect"

        # Step 2: Find nearest item
        if items_remaining == 0:
            return "wait"

        nearest_item = None
        min_distance = float("inf")

        # Scan grid for items
        for r in range(5):
            for c in range(5):
                if grid[r][c] == 1:
                    distance = abs(r - agent_row) + abs(c - agent_col)
                    # Tie-break: prefer topmost (smallest row), then leftmost (smallest col)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_item = (r, c)
                    elif distance == min_distance:
                        # Tie-break: prefer topmost (smallest row first)
                        if r < nearest_item[0]:
                            nearest_item = (r, c)
                        elif r == nearest_item[0] and c < nearest_item[1]:
                            nearest_item = (r, c)

        if nearest_item is None:
            return "wait"

        item_row, item_col = nearest_item

        # Step 3: Move toward nearest item
        if item_row < agent_row:
            return "up"
        elif item_row > agent_row:
            return "down"
        elif item_col < agent_col:
            return "left"
        elif item_col > agent_col:
            return "right"

        # Should not reach here, but return wait as fallback
        return "wait"

    def act(self, action, environment):
        """Execute action and update position if directional move succeeds."""
        valid_actions = {"up", "down", "left", "right", "collect", "wait"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}")

        # Calculate new position if directional move
        new_position = self.position
        if action == "up":
            new_position = (self.position[0] - 1, self.position[1])
        elif action == "down":
            new_position = (self.position[0] + 1, self.position[1])
        elif action == "left":
            new_position = (self.position[0], self.position[1] - 1)
        elif action == "right":
            new_position = (self.position[0], self.position[1] + 1)

        # Execute action in environment
        success = environment.step(action, self.position)

        # Update position only on successful directional moves
        if action in {"up", "down", "left", "right"} and success:
            self.position = new_position

        # Append to action history
        self.action_history.append(action)

    def observe(self, observation_dict):
        """Store observation dict."""
        self.observations = observation_dict
