from qgate_graph.graph_performance_txt import GraphPerformanceTxt
from os import path
import unittest
import logging
import shutil
import os


class TestCasePerformanceTxt(unittest.TestCase):

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
        if not os.path.isfile(path.join(prefix, TestCasePerformanceTxt.INPUT_FILE)):
            prefix=".."
        TestCasePerformanceTxt.OUTPUT_ADR = path.join(prefix,TestCasePerformanceTxt.OUTPUT_ADR)
        TestCasePerformanceTxt.INPUT_FILE = path.join(prefix, TestCasePerformanceTxt.INPUT_FILE)
        TestCasePerformanceTxt.INPUT_ADR = path.join(prefix, TestCasePerformanceTxt.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCasePerformanceTxt.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_txt1(self):
        """Performance graphs"""
        graph = GraphPerformanceTxt()
        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)

    def test_txt_raw(self):
        """Performance graphs"""
        graph = GraphPerformanceTxt(raw_format = True)
        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)