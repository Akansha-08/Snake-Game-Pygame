"""
pathfinding.py
---------------
Deterministic Breadth-First Search (BFS) pathfinding for the Snake AI.

BFS is used (not A*, not any ML/RL) because on an unweighted grid it is
guaranteed to return the SHORTEST path in terms of number of grid steps,
which is exactly what we want for "shortest safe path to the food".
"""

from collections import deque


def bfs_shortest_path(start, goal, obstacles, width, height, cell_size):
    """
    Find the shortest path from `start` to `goal` on a grid using BFS.

    Args:
        start (tuple[int, int]): (x, y) pixel coordinates of the snake's head.
        goal (tuple[int, int]): (x, y) pixel coordinates of the food.
        obstacles (set[tuple[int, int]]): set of (x, y) pixel coordinates
            that are blocked (the snake's own body, excluding the head).
        width (int): play area width in pixels.
        height (int): play area height in pixels.
        cell_size (int): size of one grid cell in pixels (SNAKE_SIZE).

    Returns:
        list[tuple[int, int]] | None:
            A list of grid coordinates from the step AFTER `start` up to and
            including `goal` (start itself is not included), or None if no
            path exists.
    """
    start = tuple(start)
    goal = tuple(goal)

    if start == goal:
        return []

    # The four cardinal moves a snake can make.
    moves = [
        (cell_size, 0),
        (-cell_size, 0),
        (0, cell_size),
        (0, -cell_size),
    ]

    visited = {start}
    queue = deque([start])
    parent = {}

    while queue:
        current = queue.popleft()

        for dx, dy in moves:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in visited:
                continue

            # Stay inside the play area.
            if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                continue

            # Treat the snake's body as an obstacle (the goal cell is always
            # allowed even if it happens to coincide with a stale obstacle
            # entry, since food never spawns on the snake).
            if neighbor in obstacles and neighbor != goal:
                continue

            visited.add(neighbor)
            parent[neighbor] = current

            if neighbor == goal:
                return _reconstruct_path(parent, start, goal)

            queue.append(neighbor)

    # No path found.
    return None


def _reconstruct_path(parent, start, goal):
    """Walk the parent chain from goal back to start and reverse it."""
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    # Drop the start cell itself; caller only needs the steps to take.
    return path[1:]