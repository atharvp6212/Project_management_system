"""Deterministic scheduling algorithms for dependency-aware projects."""

from collections import defaultdict, deque
from dataclasses import dataclass


class DependencyCycleError(ValueError):
    """Raised when the dependency graph is not a DAG."""


@dataclass(frozen=True)
class ScheduledTask:
    task_id: int
    earliest_start: int
    earliest_finish: int
    is_critical: bool


def critical_path_schedule(durations: dict[int, int], edges: list[tuple[int, int]]) -> list[ScheduledTask]:
    """Schedule a task DAG using topological sorting and critical-path analysis.

    ``edges`` contains ``(predecessor, successor)`` pairs. Complexity is
    O(V + E) time and O(V + E) space.
    """
    if any(duration <= 0 for duration in durations.values()):
        raise ValueError('Every task duration must be positive.')

    successors = defaultdict(list)
    predecessors = defaultdict(list)
    indegree = {task_id: 0 for task_id in durations}
    for predecessor, successor in edges:
        if predecessor not in durations or successor not in durations:
            raise ValueError('Every dependency must reference a known task.')
        successors[predecessor].append(successor)
        predecessors[successor].append(predecessor)
        indegree[successor] += 1

    queue = deque(sorted(task_id for task_id, degree in indegree.items() if degree == 0))
    order = []
    while queue:
        task_id = queue.popleft()
        order.append(task_id)
        for successor in successors[task_id]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)

    if len(order) != len(durations):
        raise DependencyCycleError('Task dependencies contain a cycle.')

    earliest_start = {}
    earliest_finish = {}
    for task_id in order:
        earliest_start[task_id] = max(
            (earliest_finish[p] for p in predecessors[task_id]), default=0
        )
        earliest_finish[task_id] = earliest_start[task_id] + durations[task_id]

    project_finish = max(earliest_finish.values(), default=0)
    latest_finish = {}
    latest_start = {}
    for task_id in reversed(order):
        latest_finish[task_id] = min(
            (latest_start[s] for s in successors[task_id]), default=project_finish
        )
        latest_start[task_id] = latest_finish[task_id] - durations[task_id]

    return [
        ScheduledTask(
            task_id=task_id,
            earliest_start=earliest_start[task_id],
            earliest_finish=earliest_finish[task_id],
            is_critical=earliest_start[task_id] == latest_start[task_id],
        )
        for task_id in order
    ]
