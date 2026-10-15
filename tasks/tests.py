from django.test import SimpleTestCase

from .scheduling import DependencyCycleError, critical_path_schedule


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
