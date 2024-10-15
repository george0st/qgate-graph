from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.percentile_item import PercentileItem
import os.path, os


class GraphPerformanceTxt(GraphPerformance):

    def __init__(self, min_precision=-1, max_precision=-1, raw_format=False):
        super().__init__(0, min_precision, max_precision, raw_format)

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        output_file = os.path.join(output_dir, f"TXT-{file_name}.txt")
        with open(output_file, 'w') as file:
            file.write(str(super()._create_table(percentiles)))
        return output_file
