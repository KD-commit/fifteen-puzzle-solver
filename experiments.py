"""
experiments.py - Run all experiments and collect results.
Compares A* vs IDA* across 4 heuristics and 3 difficulty levels.
"""

import sys, os, time, json, csv
sys.path.insert(0, os.path.dirname(__file__))

from puzzle import Puzzle
from heuristics import HEURISTICS
from search import astar, idastar

DIFFICULTIES = [
    ("Easy",   20,  list(range(10))),
    ("Medium", 35,  list(range(10))),
    ("Hard",   55,  list(range(10))),
]

ALGORITHMS = [
    ("A*",   astar),
    ("IDA*", idastar),
]

def run_experiments():
    records = []

    for diff_name, moves, seeds in DIFFICULTIES:
        puzzles = [Puzzle.from_random(moves, seed=s) for s in seeds]

        for h_name, h_fn in HEURISTICS.items():
            for alg_name, alg_fn in ALGORITHMS:
                total_nodes_exp  = 0
                total_nodes_gen  = 0
                total_time       = 0
                total_sol_len    = 0
                solved           = 0

                for puzzle in puzzles:
                    t0 = time.perf_counter()
                    result = alg_fn(puzzle, h_fn, h_name)
                    elapsed = time.perf_counter() - t0

                    total_nodes_exp += result.nodes_expanded
                    total_nodes_gen += result.nodes_generated
                    total_time      += elapsed
                    if result.solved:
                        solved += 1
                        total_sol_len += result.solution_length

                n = len(puzzles)
                rec = {
                    "difficulty":      diff_name,
                    "moves":           moves,
                    "heuristic":       h_name,
                    "algorithm":       alg_name,
                    "avg_nodes_exp":   round(total_nodes_exp / n),
                    "avg_nodes_gen":   round(total_nodes_gen / n),
                    "avg_time_s":      round(total_time / n, 5),
                    "avg_sol_len":     round(total_sol_len / solved, 1) if solved else None,
                    "solved":          solved,
                    "total":           n,
                }
                records.append(rec)
                print(f"[{diff_name:6s}] {alg_name:5s} + {h_name:20s} | "
                      f"nodes={rec['avg_nodes_exp']:>8,}  time={rec['avg_time_s']:.5f}s  "
                      f"solved={solved}/{n}")

    return records


def save_results(records, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    json_path = os.path.join(out_dir, "results.json")
    with open(json_path, "w") as f:
        json.dump(records, f, indent=2)

    csv_path = os.path.join(out_dir, "results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"\nResults saved to {out_dir}/")
    return records


if __name__ == "__main__":
    print("Running experiments...\n")
    records = run_experiments()
    save_results(records, os.path.join(os.path.dirname(__file__), "..", "results"))
