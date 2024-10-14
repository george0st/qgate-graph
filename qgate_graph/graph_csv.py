from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.percentile_item import PercentileItem
from prettytable import PrettyTable
import os.path, os


class GraphCsv(GraphPerformance):

    def __init__(self, min_precision=-1, max_precision=-1, raw_format=False):
        super().__init__(0, min_precision, max_precision, raw_format)

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        with open(os.path.join(output_dir, f"CSV-{file_name}.csv"), 'w', newline='') as file:
            file.write(super()._create_table(percentiles).get_csv_string(delimiter=','))
