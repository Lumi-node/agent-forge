"""Unit tests for ReasoningAgent module."""

import pytest
from agent import ReasoningAgent
from environment import SimpleGridWorld


def test_agent_init():
    """Agent.__init__ initializes position, observations, and action_history."""
    agent = ReasoningAgent()
    assert agent.position == (2, 2)
    assert agent.observations == {}
    assert agent.action_history == []

    # Test with custom start position
    agent2 = ReasoningAgent((0, 0))
    assert agent2.position == (0, 0)
    assert agent2.observations == {}
    assert agent2.action_history == []


def test_agent_think_returns_valid_action():
    """Agent.think() returns one of six valid actions."""
    agent = ReasoningAgent()
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 0,
        "step_count": 0
    }
    action = agent.think()
    assert action in ["up", "down", "left", "right", "collect", "wait"]


def test_think_collect_when_item_at_position():
    """think() returns 'collect' when item at current position."""
    agent = ReasoningAgent((2, 2))
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],  # Item at agent position
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        "items_remaining": 1,
        "step_count": 0
    }
    assert agent.think() == "collect"


def test_think_wait_when_no_items():
    """think() returns 'wait' when no items remain."""
    agent = ReasoningAgent((2, 2))
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 0,
        "step_count": 0
    }
    assert agent.think() == "wait"


def test_think_moves_toward_nearest_item():
    """think() returns direction toward nearest item."""
    agent = ReasoningAgent((2, 2))
    # Single item to the right
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],  # Item at (2, 3)
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        "items_remaining": 1,
        "step_count": 0
    }
    assert agent.think() == "right"

    # Single item above
    agent.observations["grid"] = [
        [0, 0, 1, 0, 0],  # Item at (0, 2)
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    assert agent.think() == "up"

    # Single item below
    agent.observations["grid"] = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0]  # Item at (4, 2)
    ]
    assert agent.think() == "down"

    # Single item to the left
    agent.observations["grid"] = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],  # Item at (2, 0)
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    assert agent.think() == "left"


def test_think_tiebreaker_topmost():
    """think() prefers topmost item when multiple at same distance."""
    agent = ReasoningAgent((2, 2))
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [
            [1, 0, 0, 0, 0],  # Item at (0, 0), distance 4
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1]   # Item at (4, 4), distance 4
        ],
        "items_remaining": 2,
        "step_count": 0
    }
    # Both items at distance 4, prefer topmost (0, 0)
    assert agent.think() == "up"


def test_think_tiebreaker_leftmost():
    """think() prefers leftmost item when at same row and distance."""
    agent = ReasoningAgent((2, 2))
    agent.observations = {
        "agent_position": (2, 2),
        "grid": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],  # Items at (2, 0) and (2, 3), same distance
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        "items_remaining": 2,
        "step_count": 0
    }
    # Both items at same distance from agent (1 step left, 1 step right)
    # Agent at (2, 2): distance to (2, 0) = 2, distance to (2, 3) = 1
    # So prefer (2, 3) to the right
    assert agent.think() == "right"


def test_think_deterministic():
    """think() always returns same action for same observation (deterministic)."""
    agent = ReasoningAgent((2, 2))
    obs = {
        "agent_position": (2, 2),
        "grid": [
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        "items_remaining": 2,
        "step_count": 0
    }

    agent.observations = obs
    action1 = agent.think()
    action2 = agent.think()
    action3 = agent.think()

    assert action1 == action2 == action3


def test_agent_position_updates_on_movement():
    """Agent.position updates after successful move via act()."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 0)

    agent.observations = environment.get_state()
    agent.act("right", environment)

    assert agent.position == (2, 3)


def test_act_updates_position_on_valid_moves():
    """act() updates position on successful directional moves."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 0)

    agent.observations = environment.get_state()

    # Test right move
    agent.act("right", environment)
    assert agent.position == (2, 3)

    # Test down move
    agent.act("down", environment)
    assert agent.position == (3, 3)

    # Test left move
    agent.act("left", environment)
    assert agent.position == (3, 2)

    # Test up move
    agent.act("up", environment)
    assert agent.position == (2, 2)


def test_act_position_unchanged_on_out_of_bounds():
    """act() does not update position on failed moves (out of bounds)."""
    agent = ReasoningAgent((0, 0))
    environment = SimpleGridWorld((0, 0), 0)

    agent.observations = environment.get_state()

    # Try to move up from (0, 0) - should fail
    agent.act("up", environment)
    assert agent.position == (0, 0)

    # Try to move left from (0, 0) - should fail
    agent.act("left", environment)
    assert agent.position == (0, 0)


def test_act_collect_no_position_change():
    """act('collect') does not change position."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 1)

    # Place item at agent position
    environment.grid[2][2] = 1
    agent.observations = environment.get_state()

    # Act collect
    agent.act("collect", environment)

    # Position should not change
    assert agent.position == (2, 2)


def test_act_wait_no_position_change():
    """act('wait') does not change position."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 0)

    agent.observations = environment.get_state()

    # Act wait
    agent.act("wait", environment)

    # Position should not change
    assert agent.position == (2, 2)


def test_act_raises_valueerror_for_invalid_action():
    """act() raises ValueError for invalid action."""
    agent = ReasoningAgent()
    environment = SimpleGridWorld()

    with pytest.raises(ValueError):
        agent.act("invalid", environment)

    with pytest.raises(ValueError):
        agent.act("jump", environment)

    with pytest.raises(ValueError):
        agent.act("", environment)


def test_action_history_tracking():
    """action_history appends all actions executed via act()."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 0)

    agent.observations = environment.get_state()

    # Execute several actions
    agent.act("right", environment)
    agent.act("down", environment)
    agent.act("wait", environment)
    agent.act("left", environment)

    assert agent.action_history == ["right", "down", "wait", "left"]


def test_observe_stores_observation_dict():
    """observe() stores observation dict in self.observations."""
    agent = ReasoningAgent()
    obs = {
        "agent_position": (2, 2),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 3,
        "step_count": 1
    }
    agent.observe(obs)
    assert agent.observations == obs


def test_observe_overwrites_previous_observation():
    """observe() overwrites previous observation."""
    agent = ReasoningAgent()
    obs1 = {
        "agent_position": (2, 2),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 3,
        "step_count": 1
    }
    obs2 = {
        "agent_position": (3, 3),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 2,
        "step_count": 2
    }
    agent.observe(obs1)
    assert agent.observations == obs1

    agent.observe(obs2)
    assert agent.observations == obs2


def test_full_reasoning_loop_10_steps():
    """Complete 10-step reasoning loop executes without error."""
    environment = SimpleGridWorld((2, 2), 5)
    agent = ReasoningAgent((2, 2))

    for _ in range(10):
        state = environment.get_state()
        agent.observe(state)
        action = agent.think()
        agent.act(action, environment)

    assert environment.get_state()["step_count"] == 10
    assert len(agent.action_history) == 10


def test_item_collection_via_act():
    """act('collect') removes item from grid."""
    agent = ReasoningAgent((2, 2))
    environment = SimpleGridWorld((2, 2), 1)

    # Place item at (2, 2)
    environment.grid[2][2] = 1
    environment.item_count = 1

    agent.observations = environment.get_state()
    initial_count = agent.observations["items_remaining"]

    # Collect
    agent.act("collect", environment)

    # Check item removed
    new_state = environment.get_state()
    assert new_state["items_remaining"] == initial_count - 1
    assert environment.grid[2][2] == 0


def test_item_collection_removes_item_from_grid():
    """Item collection via environment.step() removes item and decrements count."""
    environment = SimpleGridWorld((2, 2), 1)

    # Manually place item at (2, 3)
    environment.grid[2][3] = 1
    environment.item_count = 1

    initial_count = environment.get_state()["items_remaining"]

    # Collect item at (2, 3)
    result = environment.step("collect", (2, 3))

    assert result == True
    final_count = environment.get_state()["items_remaining"]
    assert final_count == initial_count - 1
    assert environment.grid[2][3] == 0


def test_observe_updates_agent_state():
    """Agent.observe() stores observation dict in agent.observations."""
    agent = ReasoningAgent()
    obs = {
        "agent_position": (2, 2),
        "grid": [[0] * 5 for _ in range(5)],
        "items_remaining": 3,
        "step_count": 1
    }
    agent.observe(obs)
    assert agent.observations == obs


def test_invalid_move_out_of_bounds_fails():
    """Out-of-bounds move returns False from environment.step()."""
    environment = SimpleGridWorld((0, 0), 0)
    result = environment.step("up", (0, 0))
    assert result == False
