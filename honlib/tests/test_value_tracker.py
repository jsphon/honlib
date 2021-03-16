import unittest

from honlib import value_tracker


class MyTestCase(unittest.TestCase):
    def test_clear(self):
        vt = value_tracker.ValueTracker()

        vt.append(0, 1)
        self.assertEqual(((0, 1),), vt.to_tuple())

        vt.clear()
        self.assertEqual(tuple(), vt.to_tuple())

    def test_bool_is_false(self):
        vt = value_tracker.ValueTracker()

        self.assertFalse(bool(vt))

    def test_bool_is_true(self):
        vt = value_tracker.ValueTracker()
        vt.append(0, 0)
        self.assertTrue(bool(vt))

    def test_append(self):
        vt = value_tracker.ValueTracker()

        vt.append(1, 2)
        vt.append(2, 2)
        vt.append(3, 4)

        result = list(vt)

        self.assertEqual(2, len(result))
        self.assertEqual(1, result[0].t)
        self.assertEqual(2, result[0].v)
        self.assertEqual(3, result[1].t)
        self.assertEqual(4, result[1].v)

    def test_to_tuple(self):
        vt = value_tracker.ValueTracker()

        vt.append(1, 2)
        vt.append(2, 2)
        vt.append(3, 4)

        result = vt.to_tuple()
        self.assertEqual(((1, 2), (3, 4)), result)


class NumberValueTrackerTestCase(unittest.TestCase):
    def test_to_tuple_of_diffs(self):
        vt = value_tracker.NumberValueTracker()

        vt.append(1, 2)
        vt.append(2, 2)
        vt.append(3, 4)

        result = vt.to_tuple_of_diffs()
        self.assertEqual(((1, 2), (3, 2)), result)


class TradedVolumeTracker(unittest.TestCase):
    def test_append(self):
        trd = {"diff": {7.2: 19.0}}
        tvt = value_tracker.TradedVolumeTracker(max_age=100)
        tvt.append(100, trd)

        result = tvt.to_tuple()
        expected = ((100, {7.2: 19.0}),)
        self.assertEqual(expected, result)

        tvt.append(101, {"diff": {7.2: 1, 7.4: 1.23}})
        result = tvt.to_tuple()
        expected = (
            (100, {7.2: 19.0}),
            (101, {7.2: 1.0, 7.4: 1.23}),
        )

        self.assertEqual(expected, result)

        # expected_cumulative = {7.2: 20, 7.4: 1.23}
        # self.assertEqual(expected_cumulative, tvt.cumulative_traded_volume)

        # test min/max values
        self.assertEqual(7.2, tvt.min())
        self.assertEqual(7.4, tvt.max())

        # This should delete the first data point
        tvt.append(201, {"diff": {7.4: 18.77, 7.8: 1.23}})

        expected = ((101, {7.2: 1.0, 7.4: 1.23}), (201, {7.4: 18.77, 7.8: 1.23}))
        self.assertEqual(expected, tvt.to_tuple())

        # test min/max values
        self.assertEqual(7.2, tvt.min())
        self.assertEqual(7.8, tvt.max())

        # 4th data point
        tvt.append(202, {"diff": {7.4: 20.0, 7.8: 1.23}})
        expected = ((201, {7.4: 18.77, 7.8: 1.23}), (202, {7.4: 20.0, 7.8: 1.23}))
        self.assertEqual(expected, tvt.to_tuple())
        self.assertEqual(7.4, tvt.min())
        self.assertEqual(7.8, tvt.max())

        tvt.tick(302)
        expected = ((202, {7.4: 20.0, 7.8: 1.23}),)
        self.assertEqual(expected, tvt.to_tuple())
        self.assertEqual(7.4, tvt.min())
        self.assertEqual(7.8, tvt.max())


class WindowedValueTracker(unittest.TestCase):
    def test_append(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(10, 2)
        vt.append(20, 3)
        vt.append(30, 4)

        result = vt.to_tuple()
        expected = ((20, 3), (30, 4))
        self.assertEqual(expected, result)

    def test_tick(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(10, 2)
        vt.append(20, 3)
        vt.append(30, 4)

        vt.tick(40)
        self.assertEqual(((30, 4),), vt.to_tuple())

        vt.tick(50)
        self.assertEqual(tuple(), vt.to_tuple())

    def test_max(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(10, 2)
        vt.append(20, 3)
        vt.append(30, 4)

        result = vt.max()
        self.assertEqual(4, result)

    def test_min(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(10, 2)
        vt.append(20, 3)
        vt.append(30, 4)

        result = vt.min()
        self.assertEqual(3, result)

    def test_median(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(0, 2)
        vt.append(6, 3)
        vt.append(10, 4)

        result = vt.median()
        self.assertEqual(2, result)

    def test_median_when_split_equally(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(0, 2.0)
        vt.append(5, 3.0)
        vt.append(10, 3.0)

        result = vt.median()
        self.assertEqual(2.5, result)

    def test_median_when_not_enough_data_split_equally(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(9, 3.0)
        vt.append(10, 3.0)

        result = vt.median()
        self.assertIsNone(result)

    def test_median_when_not_enough_data_split_equally(self):
        vt = value_tracker.WindowedValueTracker(max_age=10)

        vt.append(5, 3.0)
        vt.append(10, 3.0)

        result = vt.median()
        self.assertIsNone(result)
