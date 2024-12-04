import os
import unittest
import logging
import time
from os import path
import shutil
import glob
from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.graph_executor import GraphExecutor

class TestCaseBasic(unittest.TestCase):

    OUTPUT_ADR = "output/test/"
    INPUT_FILE = "input/prf_cassandra_02.txt"
    INPUT_FILE2 = "input/prf_cassandra-write-min-2024-08-29.txt"
    INPUT_FILE3 = "input/prf_cassandra-W1-low-2024-10-07.txt"
    INPUT_FILE4 = "input/prf_cassandra-W1-low-percentile-three-lines.txt"
    INPUT_FILE5 = "input/prf_cassandra-W2-med-percentile-one-line.txt"
    INPUT_FILE6 = "input/perf_test.txt"
    INPUT_FILE7 = "input/prf_cassandra-without-std.txt"

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
        TestCaseBasic.INPUT_FILE3 = path.join(prefix, TestCaseBasic.INPUT_FILE3)
        TestCaseBasic.INPUT_FILE4 = path.join(prefix, TestCaseBasic.INPUT_FILE4)
        TestCaseBasic.INPUT_FILE5 = path.join(prefix, TestCaseBasic.INPUT_FILE5)
        TestCaseBasic.INPUT_FILE6 = path.join(prefix, TestCaseBasic.INPUT_FILE6)
        TestCaseBasic.INPUT_FILE7 = path.join(prefix, TestCaseBasic.INPUT_FILE7)
        TestCaseBasic.INPUT_ADR = path.join(prefix, TestCaseBasic.INPUT_ADR)

        # clean directory
        shutil.rmtree(TestCaseBasic.OUTPUT_ADR, True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_perf_file(self):
        """Performance graphs"""
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 2)

    def test_perf_file2(self):
        """Performance graphs with suppress error"""
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR, suppress_error = True)

        self.assertTrue(len(output) == 2)

    def test_exec_file(self):
        """Execution graphs"""
        graph = GraphExecutor()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 11)

    def test_exec_file2(self):
        """Execution graphs with suppress error"""
        graph = GraphExecutor()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR, suppress_error = True)

        self.assertTrue(len(output) == 11)

    def test_perf_dir(self):
        """Performance graphs for dir"""
        graph = GraphPerformance()
        output = graph.generate_from_dir(TestCaseBasic.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output) == 12)

    def test_exec_dir(self):
        """Execution graphs for dir"""
        graph = GraphExecutor()
        output=graph.generate_from_dir(TestCaseBasic.INPUT_ADR, self.OUTPUT_ADR)

        self.assertTrue(len(output)==67)

    def test_check_path(self):
        """Check, dir with duration and date"""
        graph = GraphPerformance()
        output_dir = os.path.join(self.OUTPUT_ADR, "path_stability")
        output = graph.generate_from_dir(TestCaseBasic.INPUT_ADR, output_dir)
        self.assertTrue(output_dir == os.path.join(self.OUTPUT_ADR, "path_stability"))

        graph = GraphExecutor()
        output_dir = os.path.join(self.OUTPUT_ADR, "path_stability")
        output = graph.generate_from_dir(TestCaseBasic.INPUT_ADR, output_dir)
        self.assertTrue(output_dir == os.path.join(self.OUTPUT_ADR, "path_stability"))

    def test_check_path_perf(self):
        """Check, dir with duration and date for perf"""
        graph = GraphPerformance()
        output_dir = os.path.join(self.OUTPUT_ADR, "path_stability")
        output = graph.generate_from_dir(TestCaseBasic.INPUT_ADR, output_dir)

        file = glob.glob(path.join(output_dir, "1 min", "2024-08-29", f"PRF-Cassandra-write-min-*-bulk-200x10.png"))
        self.assertTrue(len(file) == 1)

    def test_check_path_exec(self):
        """Check, dir with duration and date for exec"""
        graph = GraphExecutor()
        output_dir = os.path.join(self.OUTPUT_ADR, "path_stability")
        output = graph.generate_from_dir(TestCaseBasic.INPUT_ADR, output_dir)

        file = glob.glob(path.join(output_dir, "1 min", "2024-08-29", f"EXE-Cassandra-write-min-*-bulk-200x10-plan-008x01.png"))
        self.assertTrue(len(file) == 1)

    def test_performance_graph_with_without_raw(self):
        graph = GraphPerformance(raw_format = False)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        graph = GraphPerformance(raw_format = True)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)

    def test_performance_graph_with_without_raw2(self):
        graph = GraphPerformance(raw_format = False)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE2, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        graph = GraphPerformance(raw_format = True)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE2, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)

    def test_performance_graph_with_without_raw3(self):
        graph = GraphPerformance(raw_format = False)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE3, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        graph = GraphPerformance(raw_format = True)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE3, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") != -1)

    def test_performance_graph_with_percentile1(self):
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE4, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

    def test_performance_graph_with_percentile2(self):
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE5, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

    def test_perf_file3(self):
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE6, self.OUTPUT_ADR)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

    def test_perf_onlynew1(self):
        """Test setting 'only_new'"""
        graph = GraphPerformance(only_new=True)
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE6, os.path.join(self.OUTPUT_ADR,"only_new"))
        self.assertTrue(len(output)==2)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE6, os.path.join(self.OUTPUT_ADR,"only_new"))
        self.assertTrue(len(output) == 0)

    def test_perf_without_stdev(self):
        graph = GraphPerformance()
        output = graph.generate_from_file(TestCaseBasic.INPUT_FILE7, self.OUTPUT_ADR)

        self.assertTrue(len(output)==1)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)

    def read_file_all(self, file) -> str:
        with open(file) as f:
            content = ""
            for itm in f.readlines():
                content += f"{itm.strip()}\n"
            return content[:-1]
    def test_perf_source_text(self):
        graph = GraphPerformance()
        text = self.read_file_all(TestCaseBasic.INPUT_FILE7)

        output = graph.generate_from_text(text,self.OUTPUT_ADR)

        self.assertTrue(len(output)==1)
        for file in output:
            self.assertTrue(file.find("RAW") == -1)
