"""
puzzle.py - 15-Puzzle state representation, move generation, and utilities.
"""

import random
from typing import List, Tuple, Optional

GOAL_STATE = tuple(range(1, 16)) + (0,)
SIZE = 4

MOVES = {
    'UP':    (-1, 0),
    'DOWN':  ( 1, 0),
    'LEFT':  ( 0,-1),
    'RIGHT': ( 0, 1),
}


class Puzzle:
    """Represents a single 15-puzzle state."""

    def __init__(self, tiles: Tuple[int, ...]):
        assert len(tiles) == 16, "Puzzle must have 16 tiles."
        self.tiles = tiles
        self.blank = tiles.index(0)

    @classmethod
    def goal(cls) -> "Puzzle":
        return cls(GOAL_STATE)

    @classmethod
    def from_random(cls, num_moves: int, seed: Optional[int] = None) -> "Puzzle":
        """Generate a puzzle by performing random moves from goal (always solvable)."""
        rng = random.Random(seed)
        state = list(GOAL_STATE)
        blank = state.index(0)
        prev_blank = -1
        for _ in range(num_moves):
            r, c = divmod(blank, SIZE)
            neighbors = []
            for dr, dc in MOVES.values():
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    nb = nr * SIZE + nc
                    if nb != prev_blank:
                        neighbors.append(nb)
            chosen = rng.choice(neighbors)
            state[blank], state[chosen] = state[chosen], state[blank]
            prev_blank = blank
            blank = chosen
        return cls(tuple(state))

    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    def neighbors(self) -> List[Tuple["Puzzle", str]]:
        """Return list of (new_puzzle, move_name) for all valid moves."""
        r, c = divmod(self.blank, SIZE)
        result = []
        for move, (dr, dc) in MOVES.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                tiles = list(self.tiles)
                nb = nr * SIZE + nc
                tiles[self.blank], tiles[nb] = tiles[nb], tiles[self.blank]
                result.append((Puzzle(tuple(tiles)), move))
        return result

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(self.tiles)

    def __repr__(self):
        rows = []
        for r in range(SIZE):
            row = self.tiles[r*SIZE:(r+1)*SIZE]
            rows.append(" ".join(f"{v:2d}" if v != 0 else "  " for v in row))
        return "\n".join(rows)
