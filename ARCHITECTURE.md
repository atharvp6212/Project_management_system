# Architecture and research design

The web application stores tasks and dependencies, while `tasks/scheduling.py`
contains framework-independent algorithms. This separation lets experiments run
without HTTP or database overhead.

Implemented baselines are linear-time critical-path analysis, PERT estimation,
delay-impact simulation and deterministic resource-constrained list scheduling.
The heuristic prioritizes ready tasks by critical-path finish time and assigns
the resource producing the earliest finish. It is reproducible but not claimed
to solve the NP-hard RCPSP optimally.

Use `benchmarks/scheduling_benchmark.py` to measure runtime, peak memory and
schedule length over deterministic synthetic DAGs. A future exact MILP solver
can be compared with the heuristic on small instances where optimal solutions
are computationally feasible.
