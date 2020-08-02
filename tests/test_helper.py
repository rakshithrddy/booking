#!/usr/bin/env python
import unittest
from app.helper import get_distance, generate_ticket, cost


class HelperCase(unittest.TestCase):
    def setUp(self) -> None:
        self.get_distance = get_distance
        self.cost = cost
        self.generate_ticket = generate_ticket

    def test_get_distance(self):
        distance = self.get_distance(source='Mumbai', destination='Bengaluru')
        self.assertEqual(distance, 839)
        distance = self.get_distance(source='Bengaluru', destination='Mumbai')
        self.assertEqual(distance, 839)

    def test_flight_cost(self):
        cost = self.cost(distance=1000, cost_per_km=5, operational_optimized=True)
        self.assertEqual(cost, 5000)
        cost = self.cost(distance=1000, cost_per_km=10, operational_optimized=False)
        self.assertEqual(cost, 20000)
        cost = self.cost(distance=5000, cost_per_km=5)
        self.assertEqual(cost, 25000)


if __name__ == '__main__':
    unittest.main(verbosity=2)
