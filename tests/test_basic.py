import os
import unittest
import logging
import time
from os import path
import shutil
from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.graph_executor import GraphExecutor

class TestCaseBasic(unittest.TestCase):

    OUTPUT_ADR = "output/test/"
    INPUT_FILE = "input/prf_cassandra_02.txt"
    INPUT_ADR = "input"

    PREFIX = "."

    @classmethod
    def setUpClass(cls):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)

        # setup relevant path
        prefix = "."
        if not os.path.isfile(path.join(prefix, TestCaseBasic.INPUT_FILE)):
            prefix=".."
        TestCaseBasic.OUTPUT_ADR=path.join(prefix,TestCaseBasic.OUTPUT_ADR)
        TestCaseBasic.INPUT_FILE=path.join(prefix, TestCaseBasic.INPUT_FILE)
        TestCaseBasic.INPUT_ADR=path.join(prefix, TestCaseBasic.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCaseBasic.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_perf_file(self):
        """Performance graphs"""
        graph = GraphPerformance()
        output=graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output)==3)

    def test_perf_file2(self):
        """Performance graphs with suppress error"""
        graph = GraphPerformance()
        output=graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR, suppress_error = True)

        self.assertTrue(len(output)==3)

    def test_exec_file(self):
        """Execution graphs"""
        graph = GraphExecutor()
        output=graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output)==11)

    def test_exec_file2(self):
        """Execution graphs with suppress error"""
        graph = GraphExecutor()
        output=graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR, suppress_error = True)

        self.assertTrue(len(output)==11)

    def test_perf_dir(self):
        """Performance graphs for dir"""
        graph = GraphPerformance()
        output=graph.generate_from_dir(TestCaseBasic.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output)==5)

    def test_exec_dir(self):
        """Execution graphs for dir"""
        graph = GraphExecutor()
        output=graph.generate_from_dir(TestCaseBasic.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output)==23)

