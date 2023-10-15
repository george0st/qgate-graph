import os
import unittest
import logging
import time
from os import path
import shutil
from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.graph_executor import GraphExecutor

class TestCaseBasic(unittest.TestCase):

    OUTPUT_ADR = "../output/test_basic/"
    @classmethod
    def setUpClass(cls):
        shutil.rmtree(TestCaseBasic.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_basic(self):
        """Generate graphs based in input data."""
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)

        graph = GraphPerformance()
        graph.generate_from_dir("../input", "../output")
        graph.generate_from_file("../input/prf_cassandra_02.txt", "../output")

        graph = GraphExecutor()
        graph.generate_from_dir("../input", "../output")
        graph.generate_from_file("../input/prf_cassandra_02.txt", "../output")

    #    graph.generate_from_file("input/prf_nonprod_BDP_NoSQL.txt", output)
