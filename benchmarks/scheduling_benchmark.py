"""Generate deterministic DAGs and benchmark scheduling scalability."""

import argparse
import csv
import random
import sys
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tasks.scheduling import critical_path_schedule


def generate_dag(size: int, edge_probability: float, seed: int):
    rng = random.Random(seed)
    durations = {task: rng.randint(1, 20) for task in range(size)}
    edges = [
        (left, right) for left in range(size) for right in range(left + 1, size)
        if rng.random() < edge_probability
    ]
    return durations, edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sizes', nargs='+', type=int, default=[100, 500, 1000])
    parser.add_argument('--edge-probability', type=float, default=0.01)
    parser.add_argument('--output', default='scheduling_results.csv')
    args = parser.parse_args()
    rows = []
    for size in args.sizes:
        durations, edges = generate_dag(size, args.edge_probability, seed=42)
        tracemalloc.start()
        started = time.perf_counter()
        schedule = critical_path_schedule(durations, edges)
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rows.append((size, len(edges), elapsed, peak, max(x.earliest_finish for x in schedule)))
    with open(args.output, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(('tasks', 'edges', 'seconds', 'peak_bytes', 'project_finish'))
        writer.writerows(rows)


if __name__ == '__main__':
    main()
