from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.percentile_item import PercentileItem
import os.path, os
import logging


class GraphPerformanceCsv(GraphPerformance):

    def __init__(self, min_precision=-1, max_precision=-1, raw_format=False):
        super().__init__(0, min_precision, max_precision, raw_format)
        self._output_file_format = ("CSV", ".csv")

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        output_file = os.path.join(output_dir, f"CSV{file_name}.csv")
        with open(output_file, 'w', newline='') as file:
            file.write(super()._create_table(percentiles).get_csv_string(delimiter=','))
            logging.info(f"  ... {output_file}")
        return output_file
