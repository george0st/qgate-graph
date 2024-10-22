from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.percentile_item import PercentileItem
import os.path, os
import logging


class GraphPerformanceCsv(GraphPerformance):

    def __init__(self, min_precision = -1, max_precision = -1, raw_format = False, only_new = False):
        """
        Generate performance outputs based on input data in CSV format for next processing

        :param min_precision:   minimal precision in graph (-1 is without setting)
        :param max_precision:   maximal precision in graph (-1 is without setting)
        :param raw_format:      use raw format (default is True)
        :param only_new:        generate only new/not existing outputs (default is False, rewrite/regenerate all)
        """

        super().__init__(0, min_precision, max_precision, raw_format, only_new)
        self._output_file_format = ("CSV", ".csv")

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        output_file = os.path.join(output_dir, file_name)
        with open(output_file, 'w', newline='') as file:
            file.write(super()._create_table(percentiles).get_csv_string(delimiter=','))
            logging.info(f"  ... {output_file}")
        return output_file
