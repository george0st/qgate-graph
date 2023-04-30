import os.path, os
import matplotlib.pyplot as plt
import qgate_graph.file_format as const
import qgate_graph
import json, datetime
import logging

class GraphExecutor:
    """
    Generate graph based on input data

        example::

            import qgate_graph.graph as grp
            import logging

            logging.basicConfig()
            logging.getLogger().setLevel(logging.INFO)

            graph=grp.Graph()
            graph.generate_from_dir("input_adr", "output_adr")
    """
    def __init__(self, dpi=100):
        pass

    def generate_from_dir(self, input_dir: str = "input", output_dir: str = "output"):
        """
        Generate graphs about executors in time based on input directory

        example::

            import qgate_graph.graph as grp

            graph=grp.Graph()
            graph.generate_from_dir("input_adr", "output_adr")

        :param input_dir:       Input directory (default "input")
        :param output_dir:      Output directory (default "output")
        """
        for file in os.listdir(input_dir):
            self.generate_from_file(os.path.join(input_dir, file), output_dir)
        logging.info("Done")


    def generate_from_file(self, input_file: str, output_dir: str = "output"):
        """
        Generate graphs about executors based on input input file

        :param input_file:      Input file
        :param output_dir:      Output directory (default "output")
        """
        file_name = None
        total_performance = {}
        avrg_time = {}
        std_deviation = {}
        executors = {}

        logging.info(f"Processing '{input_file}' ...")
        with open(input_file, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == '#':
                    if file_name:
                        self._show_graph(executors, total_performance, avrg_time, std_deviation, title, file_name,
                                         output_dir)
                    file_name = None
                    executors.clear()
                    total_performance.clear()
                    avrg_time.clear()
                    std_deviation.clear()
                    continue
                input_dict = json.loads(line)
                if input_dict[const.FileFormat.PRF_TYPE] == const.FileFormat.PRF_HDR_TYPE:
                    # header
                    report_date = datetime.datetime.fromisoformat(input_dict[const.FileFormat.PRF_HDR_NOW]).strftime(
                        "%Y-%m-%d %H-%M-%S")
                    label = input_dict[const.FileFormat.PRF_HDR_LABEL]
                    bulk = input_dict[const.FileFormat.PRF_HDR_BULK]
                    file_name = self._unife_file_name(f"{label}-{report_date}-bulk-{bulk[0]}x{bulk[1]}")
                    title = f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}"

                elif input_dict[const.FileFormat.PRF_TYPE] == const.FileFormat.PRF_CORE_TYPE:
                    # core
                    if input_dict[const.FileFormat.PRF_CORE_GROUP] in executors:
                        executors[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(
                            input_dict[const.FileFormat.PRF_CORE_REAL_EXECUTOR])
                        total_performance[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(
                            input_dict[const.FileFormat.PRF_CORE_TOTAL_CALL_PER_SEC])
                        avrg_time[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(
                            input_dict[const.FileFormat.PRF_CORE_AVRG_TIME])
                        std_deviation[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(
                            input_dict[const.FileFormat.PRF_CORE_STD_DEVIATION])
                    else:
                        executors[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [
                            input_dict[const.FileFormat.PRF_CORE_REAL_EXECUTOR]]
                        total_performance[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [
                            input_dict[const.FileFormat.PRF_CORE_TOTAL_CALL_PER_SEC]]
                        avrg_time[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [
                            input_dict[const.FileFormat.PRF_CORE_AVRG_TIME]]
                        std_deviation[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [
                            input_dict[const.FileFormat.PRF_CORE_STD_DEVIATION]]
