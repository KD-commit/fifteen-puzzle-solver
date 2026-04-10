# 15-Puzzle Solver — CMPUT 366 Project

Optimal solver for the 15-puzzle using **A\*** and **IDA\*** with four admissible heuristics.

## Project Structure

```
fifteen_puzzle/
├── src/
│   ├── puzzle.py        # State representation, move generation
│   ├── heuristics.py    # Misplaced Tiles, Manhattan, Linear Conflict, Enhanced LC
│   ├── search.py        # A* and IDA* implementations
│   └── experiments.py   # Experiment runner
├── results/             # JSON/CSV experiment outputs
├── report.pdf           # Project report
└── README.md
```

## How to Run

```bash
cd src
python experiments.py       # Run all experiments
```

## Heuristics Implemented

| Heuristic | Description | Dominates |
|---|---|---|
| Misplaced Tiles | Count of tiles not at goal | — |
| Manhattan Distance | Sum of tile distances to goal | Misplaced |
| Linear Conflict | Manhattan + row/col conflict penalty | Manhattan |
| Enhanced LC | Linear Conflict + fringe tile penalty | Linear Conflict |

## Algorithms

- **A\***: Optimal, complete, O(b^d) memory
- **IDA\***: Optimal, complete, O(d) memory — uses iterative deepening on f-cost threshold

## Requirements

Python 3.8+ (no external dependencies for solver)
```bash
pip install reportlab   # Only needed to regenerate report PDF
```
