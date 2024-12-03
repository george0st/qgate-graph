import unittest
import numpy as np
from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.graph_setup import GraphSetup

class TestCaseBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_point_in_graph(self):
        """Performance graphs"""
        graph = GraphPerformance(min_precision=0, max_precision=4)

        precision = graph._expected_round(np.array([1, 5, 10]))
        self.assertTrue(precision == 0)

        precision = graph._expected_round(np.array([169488.92444, 0.00169488924, 0.000169488924]))
        self.assertTrue(precision == 2)
        precision = graph._expected_round(np.array([1.6948892444e+5, 1.6948892444e-3, 1.6948892444e-4]))
        self.assertTrue(precision == 2)

        precision = graph._expected_round(np.array([0.001302153310812064, 0.00327365633422423, 0.0092585296234321431]))
        self.assertTrue(precision == 3)

        precision = graph._expected_round(np.array([1.552, 1.545, 1.547]))
        self.assertTrue(precision == 3)

        precision = graph._expected_round(np.array([0.001302153310812064, 0.00127365633422423, 0.0012585296234321431]))
        self.assertTrue(precision == 4)

        precision = graph._expected_round(np.array([1.552, 1.54599, 1.547]))
        self.assertTrue(precision >= 3)

        precision = graph._expected_round(np.array([1.1, 1.0, 1.3]))
        self.assertTrue(precision == 1)

    def test_graph_setup(self):
        GraphSetup().response_time_unit="JS"
        print(GraphSetup().response_time_unit)