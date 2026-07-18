"""
utils.py
--------
Small, reusable helpers for grid/direction math used by the AI agent.
Kept separate from ai_agent.py so the decision logic stays readable.
"""

from src.settings import SNAKE_SIZE, WIDTH, HEIGHT, TOP_BAR_HEIGHT

# The four possible movement vectors on the grid.
DIRECTIONS = [
    (SNAKE_SIZE, 0),   # right
    (-SNAKE_SIZE, 0),  # left
    (0, SNAKE_SIZE),   # down
    (0, -SNAKE_SIZE),  # up
]


def direction_between(point_a, point_b):
    """
    Return the (dx, dy) movement vector needed to go from point_a to the
    adjacent point_b (both are (x, y) pixel coordinates).
    """
    return (point_b[0] - point_a[0], point_b[1] - point_a[1])


def is_within_bounds(point):
    """
    Check whether a (x, y) point lies inside the actual playable area —
    this excludes the top status ribbon, which is off-limits even though
    it isn't drawn as a wall.
    """
    x, y = point
    return 0 <= x < WIDTH and TOP_BAR_HEIGHT <= y < HEIGHT


def is_safe_move(point, obstacles):
    """
    A move is safe if it stays on the board and doesn't land on the
    snake's own body.
    """
    return is_within_bounds(point) and tuple(point) not in obstacles


def opposite_direction(dx, dy):
    """Return the reverse of a movement vector."""
    return (-dx, -dy)