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
        """Performance graphs txt """
        graph = GraphPerformanceTxt()
        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

    def test_txt_raw(self):
        """Performance graphs txt with RAW format"""
        graph = GraphPerformanceTxt(raw_format = True)
        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)
            self.assertTrue(file.find("TXT-PRF-") == -1)

    def test_txt_from_dir_with_raw(self):
        """Performance graphs txt with RAW format"""
        graph = GraphPerformanceTxt(raw_format = True)
        output = graph.generate_from_dir(TestCasePerformanceTxt.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 12)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)
            self.assertTrue(file.find("TXT-PRF-") == -1)

    def test_txt_from_dir(self):
        """Performance graphs txt"""
        graph = GraphPerformanceTxt()
        output = graph.generate_from_dir(TestCasePerformanceTxt.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 12)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)
            self.assertTrue(file.find("TXT-PRF-") == -1)

    def test_perf_txt_onlynew1(self):
        """Test setting 'only_new'"""
        graph = GraphPerformanceTxt(only_new=True)
        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, os.path.join(self.OUTPUT_ADR,"only_new"))
        self.assertTrue(len(output)==2)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        output = graph.generate_from_file(TestCasePerformanceTxt.INPUT_FILE, os.path.join(self.OUTPUT_ADR,"only_new"))
        self.assertTrue(len(output) == 0)