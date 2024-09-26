import unittest
import numpy as np
from qgate_graph.graph_performance import GraphPerformance

class TestCaseBasic(unittest.TestCase):

    OUTPUT_ADR = "output/test/"
    INPUT_FILE = "input/prf_cassandra_02.txt"
    INPUT_ADR = "input"

    PREFIX = "."

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_point_in_graph(self):
        """Performance graphs"""
        graph = GraphPerformance(min_precision=0, max_precision=4)

        precision = graph.expected_round(np.array([1.552, 1.545, 1.547]))
        self.assertTrue(precision == 3)

        precision = graph.expected_round(np.array([1.1, 1.0, 1.3]))
        self.assertTrue(precision == 1)

        precision = graph.expected_round(np.array([1, 5, 10]))
        self.assertTrue(precision == 0)