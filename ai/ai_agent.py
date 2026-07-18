"""
ai_agent.py
-----------
Deterministic AI agent for the Snake game.

Decision process (no machine learning / reinforcement learning involved):
  1. Every frame, run BFS from the snake's head to the food, treating the
     snake's own body as obstacles.
  2. If a path exists, take one step along it.
  3. If no path exists (e.g. the snake would trap itself), fall back to a
     simple survival strategy: pick any adjacent cell that doesn't hit a
     wall or the snake's own body, preferring to keep going straight.
  4. If truly no safe move exists, a collision is unavoidable and the
     current direction is kept (the game's own collision handling takes
     over from there).
"""

from ai.pathfinding import bfs_shortest_path
from ai.utils import DIRECTIONS, direction_between, is_safe_move, opposite_direction
from src.settings import SNAKE_SIZE, WIDTH, HEIGHT


class AIAgent:
    """Wraps BFS pathfinding + fallback logic into a single decision call."""

    def __init__(self):
        # Stores the most recently computed path, purely so the game can
        # optionally draw it on screen for visualization.
        self.current_path = []

    def get_next_direction(self, snake, food):
        """
        Compute the (dx, dy) direction the snake should move this frame.
        """
        head = tuple(snake.body[-1])
        goal = (food.x, food.y)

        # The body (excluding the head) is what the snake must avoid.
        body_cells = {tuple(block) for block in list(snake.body)[:-1]}

        path = bfs_shortest_path(head, goal, body_cells, WIDTH, HEIGHT, SNAKE_SIZE)
        current_dir = (snake.x_change, snake.y_change)

        if path:
            self.current_path = path
            next_cell = path[0]
            return direction_between(head, next_cell)

        # No path to the food right now -> survive using the fallback.
        self.current_path = []
        return self._fallback_move(head, current_dir, body_cells)

    def _fallback_move(self, head, current_dir, body_cells):
        """
        Choose any move that keeps the snake alive this frame when no path
        to the food currently exists.
        """
        safe_candidates = []

        for dx, dy in DIRECTIONS:
            # Never allow an instant 180-degree reversal into your own neck.
            if current_dir != (0, 0) and (dx, dy) == opposite_direction(*current_dir):
                continue

            next_point = (head[0] + dx, head[1] + dy)
            if is_safe_move(next_point, body_cells):
                safe_candidates.append((dx, dy))

        if not safe_candidates:
            # No safe move exists at all; a collision is unavoidable.
            return current_dir if current_dir != (0, 0) else DIRECTIONS[0]

        # Prefer continuing straight for smoother, less erratic movement.
        if current_dir in safe_candidates:
            return current_dir

        return safe_candidates[0]