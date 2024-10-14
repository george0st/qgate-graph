import os
import unittest
import logging
import time
from os import path
import shutil
import glob
from qgate_graph.graph_performance_txt import GraphPerformanceTxt

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
        TestCaseBasic.OUTPUT_ADR = path.join(prefix,TestCaseBasic.OUTPUT_ADR)
        TestCaseBasic.INPUT_FILE = path.join(prefix, TestCaseBasic.INPUT_FILE)
        TestCaseBasic.INPUT_ADR = path.join(prefix, TestCaseBasic.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCaseBasic.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_txt1(self):
        """Performance graphs"""
        graph = GraphPerformanceTxt()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)
