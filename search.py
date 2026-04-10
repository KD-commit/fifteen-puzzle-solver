"""
search.py - A* and IDA* search algorithms for the 15-puzzle.

Both algorithms are complete and optimal when given an admissible heuristic.
IDA* trades memory for time: O(d) space vs O(b^d) for A*.
"""

import heapq
from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple
from puzzle import Puzzle

NODE_LIMIT = 1_000_000


@dataclass
class SearchResult:
    solved: bool
    solution_length: Optional[int]
    nodes_expanded: int
    nodes_generated: int
    algorithm: str
    heuristic_name: str


# ─── A* ──────────────────────────────────────────────────────────────────────

def astar(start: Puzzle, heuristic: Callable, h_name: str = "") -> SearchResult:
    """
    A* search. Optimal and complete with admissible + consistent heuristic.
    Uses a min-heap on f = g + h. Tracks best known g to prune duplicates.
    """
    h0 = heuristic(start)
    # (f, g, state_tiles) — tiles used instead of Puzzle to keep heap fast
    open_heap = [(h0, 0, start.tiles)]
    best_g = {start.tiles: 0}
    nodes_expanded = 0
    nodes_generated = 1

    while open_heap:
        f, g, tiles = heapq.heappop(open_heap)
        state = Puzzle(tiles)

        if g > best_g.get(tiles, float('inf')):
            continue  # Stale entry

        if state.is_goal():
            return SearchResult(True, g, nodes_expanded, nodes_generated, "A*", h_name)

        if nodes_expanded >= NODE_LIMIT:
            return SearchResult(False, None, nodes_expanded, nodes_generated, "A*", h_name)

        nodes_expanded += 1

        for neighbor, _ in state.neighbors():
            ng = g + 1
            if ng < best_g.get(neighbor.tiles, float('inf')):
                best_g[neighbor.tiles] = ng
                nh = heuristic(neighbor)
                heapq.heappush(open_heap, (ng + nh, ng, neighbor.tiles))
                nodes_generated += 1

    return SearchResult(False, None, nodes_expanded, nodes_generated, "A*", h_name)


# ─── IDA* ─────────────────────────────────────────────────────────────────────

def idastar(start: Puzzle, heuristic: Callable, h_name: str = "") -> SearchResult:
    """
    IDA* (Iterative Deepening A*). Memory-efficient optimal search.
    Performs depth-first search with an f-cost threshold that increases
    each iteration to the minimum exceeded f-value found.
    """
    threshold = heuristic(start)
    nodes_expanded = 0
    nodes_generated = 1

    def search(tiles, g, threshold, prev_tiles):
        nonlocal nodes_expanded, nodes_generated
        state = Puzzle(tiles)
        f = g + heuristic(state)

        if f > threshold:
            return f  # Signal next threshold

        if state.is_goal():
            return -1  # Found

        if nodes_expanded >= NODE_LIMIT:
            return float('inf')

        nodes_expanded += 1
        minimum = float('inf')

        for neighbor, _ in state.neighbors():
            if neighbor.tiles == prev_tiles:
                continue  # Avoid immediate backtrack
            nodes_generated += 1
            result = search(neighbor.tiles, g + 1, threshold, tiles)
            if result == -1:
                return -1
            if result < minimum:
                minimum = result

        return minimum

    import sys
    sys.setrecursionlimit(200000)

    for _ in range(200):  # Max iterations
        result = search(start.tiles, 0, threshold, None)
        if result == -1:
            return SearchResult(True, threshold, nodes_expanded, nodes_generated, "IDA*", h_name)
        if result == float('inf'):
            return SearchResult(False, None, nodes_expanded, nodes_generated, "IDA*", h_name)
        threshold = result

    return SearchResult(False, None, nodes_expanded, nodes_generated, "IDA*", h_name)
