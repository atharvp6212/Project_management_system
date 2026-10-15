"""Deterministic scheduling algorithms for dependency-aware projects."""

from collections import defaultdict, deque
from dataclasses import dataclass
from math import sqrt


class DependencyCycleError(ValueError):
    """Raised when the dependency graph is not a DAG."""


@dataclass(frozen=True)
class ScheduledTask:
    task_id: int
    earliest_start: int
    earliest_finish: int
    is_critical: bool


@dataclass(frozen=True)
class ResourceTask:
    task_id: int
    start: int
    finish: int
    resource: str


def pert_estimate(optimistic: float, most_likely: float, pessimistic: float) -> tuple[float, float]:
    """Return PERT expected duration and standard deviation."""
    if not 0 < optimistic <= most_likely <= pessimistic:
        raise ValueError('PERT estimates must satisfy 0 < O <= M <= P.')
    return ((optimistic + 4 * most_likely + pessimistic) / 6, (pessimistic - optimistic) / 6)


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


def resource_constrained_schedule(
    durations: dict[int, int],
    edges: list[tuple[int, int]],
    eligible_resources: dict[int, set[str]],
) -> list[ResourceTask]:
    """Greedy list scheduling with precedence and resource constraints.

    Ready tasks are prioritized by their critical-path finish time. The
    implementation is deterministic and intended as a reproducible heuristic
    baseline; it does not claim an optimal RCPSP solution.
    """
    baseline = critical_path_schedule(durations, edges)
    priority = {row.task_id: row.earliest_finish for row in baseline}
    predecessors = defaultdict(set)
    successors = defaultdict(set)
    for predecessor, successor in edges:
        predecessors[successor].add(predecessor)
        successors[predecessor].add(successor)
    if set(eligible_resources) != set(durations) or any(not value for value in eligible_resources.values()):
        raise ValueError('Every task must have at least one eligible resource.')

    unscheduled = set(durations)
    finish_times: dict[int, int] = {}
    resource_free = {resource: 0 for values in eligible_resources.values() for resource in values}
    result = []
    while unscheduled:
        ready = [task for task in unscheduled if predecessors[task] <= finish_times.keys()]
        if not ready:
            raise DependencyCycleError('Task dependencies contain a cycle.')
        task = max(ready, key=lambda value: (priority[value], -value))
        dependency_finish = max((finish_times[p] for p in predecessors[task]), default=0)
        resource = min(
            eligible_resources[task],
            key=lambda value: (max(dependency_finish, resource_free[value]), value),
        )
        start = max(dependency_finish, resource_free[resource])
        finish = start + durations[task]
        result.append(ResourceTask(task, start, finish, resource))
        resource_free[resource] = finish
        finish_times[task] = finish
        unscheduled.remove(task)
    return sorted(result, key=lambda row: (row.start, row.task_id))


def delayed_project_finish(
    durations: dict[int, int], edges: list[tuple[int, int]], task_id: int, delay: int
) -> int:
    """Return projected completion time after delaying one task."""
    if task_id not in durations or delay < 0:
        raise ValueError('Use a known task and a non-negative delay.')
    changed = dict(durations)
    changed[task_id] += delay
    return max((row.earliest_finish for row in critical_path_schedule(changed, edges)), default=0)
