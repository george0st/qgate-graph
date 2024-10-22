import os
import unittest
import logging
from os import path
import shutil
from qgate_graph.graph_executor import GraphExecutor


class TestCaseExecutor(unittest.TestCase):

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
        if not os.path.isfile(path.join(prefix, TestCaseExecutor.INPUT_FILE)):
            prefix=".."
        TestCaseExecutor.OUTPUT_ADR = path.join(prefix,TestCaseExecutor.OUTPUT_ADR)
        TestCaseExecutor.INPUT_FILE = path.join(prefix, TestCaseExecutor.INPUT_FILE)
        TestCaseExecutor.INPUT_ADR = path.join(prefix, TestCaseExecutor.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCaseExecutor.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_executor_onlynew1(self):
        """Test setting 'only_new'"""
        graph = GraphExecutor(only_new=True)
        output = graph.generate_from_file(TestCaseExecutor.INPUT_FILE, self.OUTPUT_ADR)
        self.assertTrue(len(output) == 11)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        output = graph.generate_from_file(TestCaseExecutor.INPUT_FILE, self.OUTPUT_ADR)
        self.assertTrue(len(output) == 0)