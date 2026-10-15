from django.test import SimpleTestCase

from .scheduling import (
    DependencyCycleError, critical_path_schedule, delayed_project_finish,
    pert_estimate, resource_constrained_schedule,
)


class CriticalPathTests(SimpleTestCase):
    def test_calculates_earliest_times_and_critical_path(self):
        schedule = critical_path_schedule(
            {1: 3, 2: 2, 3: 4, 4: 1},
            [(1, 3), (2, 3), (3, 4)],
        )
        by_id = {row.task_id: row for row in schedule}
        self.assertEqual(by_id[3].earliest_start, 3)
        self.assertEqual(by_id[4].earliest_finish, 8)
        self.assertTrue(by_id[1].is_critical)
        self.assertFalse(by_id[2].is_critical)

    def test_rejects_cycles(self):
        with self.assertRaises(DependencyCycleError):
            critical_path_schedule({1: 1, 2: 1}, [(1, 2), (2, 1)])

    def test_rejects_non_positive_duration(self):
        with self.assertRaisesMessage(ValueError, 'positive'):
            critical_path_schedule({1: 0}, [])

    def test_resource_scheduler_never_double_books_a_worker(self):
        rows = resource_constrained_schedule(
            {1: 3, 2: 2, 3: 1}, [], {1: {'A'}, 2: {'A'}, 3: {'B'}}
        )
        worker_a = sorted((row.start, row.finish) for row in rows if row.resource == 'A')
        self.assertGreaterEqual(worker_a[1][0], worker_a[0][1])

    def test_delay_impact_and_pert(self):
        self.assertEqual(delayed_project_finish({1: 2, 2: 3}, [(1, 2)], 1, 4), 9)
        mean, deviation = pert_estimate(2, 5, 8)
        self.assertEqual((mean, deviation), (5, 1))
