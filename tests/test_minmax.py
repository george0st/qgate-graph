import os
import unittest
import logging
import time
from os import path
import shutil
import glob
from qgate_graph.graph_performance_csv import GraphPerformanceCsv
from qgate_graph.graph_executor import GraphExecutor

class TestCaseBasic(unittest.TestCase):

    OUTPUT_ADR = "output/test/"
    INPUT_FILE = "input/perf_gil_impact_percentile.txt"
    INPUT_FILE2 = "input/perf_test.txt"

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
        TestCaseBasic.OUTPUT_ADR = path.join(prefix,TestCaseBasic.OUTPUT_ADR)
        TestCaseBasic.INPUT_FILE = path.join(prefix, TestCaseBasic.INPUT_FILE)
        TestCaseBasic.INPUT_FILE2 = path.join(prefix, TestCaseBasic.INPUT_FILE2)
        TestCaseBasic.INPUT_ADR = path.join(prefix, TestCaseBasic.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCaseBasic.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_minmax_with(self):
        graph = GraphPerformanceCsv()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)
        for file in output:
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Min") != -1 and line.find("Min 9") != -1
                                and line.find("Max") != -1 and line.find("Max 9") != 1)

    def test_minmax_without(self):
        graph = GraphPerformanceCsv()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE2, self.OUTPUT_ADR)
        for file in output:
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Min") == -1 and line.find("Max") == -1)
