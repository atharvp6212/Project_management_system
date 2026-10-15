# Dependency-Aware Project Scheduling and Resource Optimization System

A Django project-management application for groups, projects, task assignment,
deadlines and notifications. The scheduling module models task dependencies as a
directed acyclic graph and computes earliest start times and the critical path.

It now also includes PERT estimates, delay-impact analysis, resource-constrained
list scheduling and a deterministic scalability benchmark.

## Algorithmic component

The scheduler uses Kahn's topological-sort algorithm followed by forward and
backward passes for critical-path analysis. For `V` tasks and `E` dependencies,
the algorithm runs in `O(V + E)` time and uses `O(V + E)` space. Cyclic graphs,
unknown tasks and invalid durations are rejected explicitly.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Reproducible evaluation

Run `python benchmarks/scheduling_benchmark.py --sizes 100 500 1000`. The CSV
captures runtime, peak memory, graph size and project completion time. See
`ARCHITECTURE.md` for the research design and `LIMITATIONS.md` before making
claims from the results.
