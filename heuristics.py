"""
heuristics.py - Admissible heuristics for the 15-puzzle.

All heuristics h(n) satisfy h(n) <= h*(n) (admissibility) and
h(n) <= c(n,n') + h(n') (consistency), ensuring A* optimality.
"""

from puzzle import GOAL_STATE, SIZE

# Precompute goal positions for fast lookup
GOAL_POS = {v: divmod(i, SIZE) for i, v in enumerate(GOAL_STATE)}


def misplaced_tiles(puzzle) -> int:
    """
    h1: Count of tiles not in their goal position.
    Weakest heuristic — ignores how far tiles need to travel.
    """
    return sum(
        1 for i, v in enumerate(puzzle.tiles)
        if v != 0 and v != GOAL_STATE[i]
    )


def manhattan_distance(puzzle) -> int:
    """
    h2: Sum of Manhattan distances of each tile to its goal position.
    Dominates misplaced tiles: h2(n) >= h1(n) for all n.
    """
    dist = 0
    for i, v in enumerate(puzzle.tiles):
        if v == 0:
            continue
        gr, gc = GOAL_POS[v]
        cr, cc = divmod(i, SIZE)
        dist += abs(gr - cr) + abs(gc - cc)
    return dist


def linear_conflict(puzzle) -> int:
    """
    h3: Manhattan Distance + Linear Conflict penalty.

    Two tiles tj, tk are in linear conflict in a row if:
      - Both are in the same row
      - Both belong in that row (goal row == current row)
      - tj is to the right of tk but goal(tj) < goal(tk)
    Each conflict adds 2 moves (one tile must step out and back).
    Dominates manhattan: h3(n) >= h2(n) for all n.
    """
    h = manhattan_distance(puzzle)
    tiles = puzzle.tiles

    # Row conflicts
    for r in range(SIZE):
        row_vals = [tiles[r * SIZE + c] for c in range(SIZE)]
        in_row = [(v, GOAL_POS[v][1]) for v in row_vals
                  if v != 0 and GOAL_POS[v][0] == r]
        for i in range(len(in_row)):
            for j in range(i + 1, len(in_row)):
                if in_row[i][1] > in_row[j][1]:
                    h += 2

    # Column conflicts
    for c in range(SIZE):
        col_vals = [tiles[r * SIZE + c] for r in range(SIZE)]
        in_col = [(v, GOAL_POS[v][0]) for v in col_vals
                  if v != 0 and GOAL_POS[v][1] == c]
        for i in range(len(in_col)):
            for j in range(i + 1, len(in_col)):
                if in_col[i][1] > in_col[j][1]:
                    h += 2

    return h


def walking_distance(puzzle) -> int:
    """
    h4: Pattern database approximation using row/column walking distance.
    Uses fringe tiles heuristic as a further enhancement over linear conflict.
    Considers tiles on the last row and last column separately.
    """
    base = linear_conflict(puzzle)
    tiles = puzzle.tiles

    # Last row penalty: tiles that belong in last row but aren't there
    last_row_penalty = 0
    for c in range(SIZE):
        v = tiles[(SIZE-1)*SIZE + c]
        if v != 0:
            gr, gc = GOAL_POS[v]
            if gr != SIZE - 1:
                last_row_penalty += 1

    # Last col penalty
    last_col_penalty = 0
    for r in range(SIZE):
        v = tiles[r*SIZE + (SIZE-1)]
        if v != 0:
            gr, gc = GOAL_POS[v]
            if gc != SIZE - 1:
                last_col_penalty += 1

    return base + max(0, last_row_penalty - 1) + max(0, last_col_penalty - 1)


HEURISTICS = {
    "Misplaced Tiles":   misplaced_tiles,
    "Manhattan":         manhattan_distance,
    "Linear Conflict":   linear_conflict,
    "Enhanced LC":       walking_distance,
}
