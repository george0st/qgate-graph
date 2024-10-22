import os
import unittest
import logging
import time
from os import path
import shutil
import glob
from qgate_graph.graph_performance_csv import GraphPerformanceCsv


class TestCasePerformanceCsv(unittest.TestCase):

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
        if not os.path.isfile(path.join(prefix, TestCasePerformanceCsv.INPUT_FILE)):
            prefix=".."
        TestCasePerformanceCsv.OUTPUT_ADR = path.join(prefix,TestCasePerformanceCsv.OUTPUT_ADR)
        TestCasePerformanceCsv.INPUT_FILE = path.join(prefix, TestCasePerformanceCsv.INPUT_FILE)
        TestCasePerformanceCsv.INPUT_ADR = path.join(prefix, TestCasePerformanceCsv.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCasePerformanceCsv.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_csv1(self):
        """Performance graphs csv"""
        graph = GraphPerformanceCsv()
        output = graph.generate_from_file(TestCasePerformanceCsv.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

            # check header
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Executors") != -1 and line.find("Group") != -1 and
                                line.find("Performance") != -1 and line.find("Avrg") != 1 and
                                line.find("Std") != -1)


    def test_csv_raw(self):
        """Performance graphs csv with RAW format"""
        graph = GraphPerformanceCsv(raw_format = True)
        output = graph.generate_from_file(TestCasePerformanceCsv.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)
            self.assertTrue(file.find("CSV-PRF-") == -1)

            # check header
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Executors") != -1 and line.find("Group") != -1 and
                                line.find("Performance") != -1 and line.find("Avrg") != 1 and
                                line.find("Std") != -1)

    def test_csv_from_dir_with_raw(self):
        """Performance graphs csv with RAW format"""
        graph = GraphPerformanceCsv(raw_format=True)
        output = graph.generate_from_dir(TestCasePerformanceCsv.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 12)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)
            self.assertTrue(file.find("CSV-PRF-") == -1)

            # check header
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Executors") != -1 and line.find("Group") != -1 and
                                line.find("Performance") != -1 and line.find("Avrg") != 1 and
                                line.find("Std") != -1)

    def test_csv_from_dir(self):
        """Performance graphs csv"""
        graph = GraphPerformanceCsv()
        output = graph.generate_from_dir(TestCasePerformanceCsv.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 12)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)
            self.assertTrue(file.find("CSV-PRF-") == -1)

            # check header
            with open(file,"r") as f:
                line=f.readline()
                self.assertTrue(line.find("Executors") != -1 and line.find("Group") != -1 and
                                line.find("Performance") != -1 and line.find("Avrg") != 1 and
                                line.find("Std") != -1)

    def test_perf_csv_onlynew1(self):
        """Test setting 'only_new'"""
        graph = GraphPerformanceCsv(only_new=True)
        output = graph.generate_from_file(TestCasePerformanceCsv.INPUT_FILE, self.OUTPUT_ADR)
        self.assertTrue(len(output)==2)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        output = graph.generate_from_file(TestCasePerformanceCsv.INPUT_FILE, self.OUTPUT_ADR)
        self.assertTrue(len(output) == 0)
