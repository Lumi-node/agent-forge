"""SimpleGridWorld: 5×5 grid environment with item tracking and movement validation."""


class SimpleGridWorld:
    """5×5 grid world with item tracking and state management."""

    def __init__(self, agent_pos: tuple[int, int] = (2, 2), num_items: int = 5) -> None:
        """Initialize 5×5 grid with items at fixed positions."""
        self.grid = [[0 for _ in range(5)] for _ in range(5)]
        self.agent_pos = agent_pos
        self.item_count = num_items
        self.step_count = 0

        # Deterministic item placement at fixed positions
        # Items placed at: (0,0), (0,4), (2,0), (4,0), (4,4)
        # Never placed at agent_pos
        fixed_positions = [(0, 0), (0, 4), (2, 0), (4, 0), (4, 4)]
        items_placed = 0
        for pos in fixed_positions:
            if items_placed >= num_items:
                break
            if pos != agent_pos:
                self.grid[pos[0]][pos[1]] = 1
                items_placed += 1

    def step(self, action: str, agent_pos: tuple[int, int]) -> bool:
        """Execute action and return success status."""
        if action == "up":
            new_pos = (agent_pos[0] - 1, agent_pos[1])
            if self.is_valid_position(new_pos):
                self.step_count += 1
                return True
            return False

        elif action == "down":
            new_pos = (agent_pos[0] + 1, agent_pos[1])
            if self.is_valid_position(new_pos):
                self.step_count += 1
                return True
            return False

        elif action == "left":
            new_pos = (agent_pos[0], agent_pos[1] - 1)
            if self.is_valid_position(new_pos):
                self.step_count += 1
                return True
            return False

        elif action == "right":
            new_pos = (agent_pos[0], agent_pos[1] + 1)
            if self.is_valid_position(new_pos):
                self.step_count += 1
                return True
            return False

        elif action == "collect":
            if self.grid[agent_pos[0]][agent_pos[1]] == 1:
                self.grid[agent_pos[0]][agent_pos[1]] = 0
                self.item_count -= 1
                self.step_count += 1
                return True
            return False

        elif action == "wait":
            self.step_count += 1
            return True

        else:
            return False

    def get_state(self) -> dict:
        """Return current environment state dict."""
        return {
            "agent_position": self.agent_pos,
            "grid": self.grid,
            "items_remaining": self.item_count,
            "step_count": self.step_count,
        }

    def is_valid_position(self, pos: tuple[int, int]) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= pos[0] < 5 and 0 <= pos[1] < 5
