# Dependency-Aware Project Scheduling and Resource Optimization System

A Django project-management application for groups, projects, task assignment,
deadlines and notifications. The scheduling module models task dependencies as a
directed acyclic graph and computes earliest start times and the critical path.

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

## Planned evaluation

Future experiments will compare FIFO, earliest-deadline-first and critical-path-
aware scheduling using project completion time, missed deadlines and workload
balance as metrics.
