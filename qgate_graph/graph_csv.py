from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.percentile_item import PercentileItem
from prettytable import PrettyTable
import os.path, os


class GraphCsv(GraphPerformance):

    def __init__(self, min_precision=-1, max_precision=-1, raw_format=False):
        super().__init__(0, min_precision, max_precision, raw_format)

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        return self._create_table(percentiles, title, file_name, output_dir)

    def _create_table(self, percentiles: {PercentileItem}, title, file_name, output_dir):
        summary_table = PrettyTable()

        percentiles_sort = sorted(list(percentiles.keys()))
        for label in percentiles[1].executors.keys():
            table = PrettyTable()
            table.add_column("Executors", percentiles[1].executors[label])
            table.add_column("Label", [label]*len(percentiles[1].executors[label]))
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Performance{suffix}", percentiles[percentile].total_performance[label])
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Avrg{suffix}", percentiles[percentile].avrg_time[label])
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Std{suffix}", percentiles[percentile].std_deviation[label])

            if len(summary_table.rows) == 0:
                summary_table = table
            else:
                summary_table.add_rows(table.rows)

        summary_table.border = True
        summary_table.header = True
        summary_table.padding_width = 1
        summary_table.align = "r"
        summary_table.align["Executors"] = "c"
        summary_table.align["Label"] = "l"

        with open(os.path.join(output_dir, f"CSV-{file_name}.csv"), 'w', newline='') as file:
            file.write(summary_table.get_csv_string(delimiter=','))