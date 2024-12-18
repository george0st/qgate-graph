from qgate_graph import __version__ as version
from matplotlib import get_backend, use
from qgate_graph.percentile_item import PercentileItem
from prettytable import PrettyTable
import json


class GraphBase:
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
        self.dpi=dpi

        # use 'Agg' as non-interactive backend for matplotlib
        if get_backend().lower()!="agg":
            use('Agg', force = True)

    def _watermark(self, plt, ax):
        """
        Add watermark to the graph
        :param plt:
        :param ax:
        """
        watermark=f'qgate_graph (v{version})'
        plt.text(1.0, 0, watermark,
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 transform = ax.transAxes,
                 alpha=0.4, fontsize=8)

    def _unique_file_name(self, prefix, label, report_date, bulk, raw_format = False, extension = None):
        """
        Generate unique file name based on key information

        :param prefix:      Optional name
        :param label:       Label (typically from perf test)
        :param report_date: Report date
        :param bulk:        Bulk (rows, columns) size
        :raw_format:        True - for RAW
        :extension:         File extension such as ".png", ".txt", etc. (None - without extension)
        :return:            Return unique file name
        """
        file_name=(f"{prefix}"
                   f"-{label}"
                   f"{'-RAW' if raw_format else ''}"
                   f"-{report_date}"
                   f"-bulk-{bulk[0]}x{bulk[1]}"
                   f"{extension if extension else ''}")

        # unify names
        remove_item = " ,&?"
        for itm in remove_item:
            file_name = file_name.replace(itm,"_")
        return file_name.replace("__","_")

    def _readable_duration(self, duration_seconds):
        """Return duration in human-readable form"""

        if duration_seconds < 0:
            return "n/a"

        str_duration = []
        days = duration_seconds // 86400
        if days > 0:
            str_duration.append(f"{days} day")
        hours = duration_seconds // 3600 % 24
        if hours > 0:
            str_duration.append(f"{hours} hour")
        minutes = duration_seconds // 60 % 60
        if minutes > 0:
            str_duration.append(f"{minutes} min")
        seconds = duration_seconds % 60
        if seconds > 0:
            str_duration.append(f"{seconds} sec")
        return ' '.join(str_duration)

    @staticmethod
    def load_json(line):
        try:
            return json.loads(line.strip())
        except Exception as ex:
            pass

    def _create_table(self, percentiles: {PercentileItem}) -> PrettyTable:
        summary_table = PrettyTable()

        percentiles_sort = sorted(list(percentiles.keys()))
        for group in percentiles[1].executors.keys():
            table = PrettyTable()
            table.add_column("Executors", percentiles[1].executors[group])
            table.add_column("Group", [group]*len(percentiles[1].executors[group]))
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Performance{suffix}", percentiles[percentile].total_performance[group])
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Avrg{suffix}", percentiles[percentile].avrg_time[group])
            for percentile in percentiles_sort:
                suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                table.add_column(f"Std{suffix}", percentiles[percentile].std_deviation[group])

            for percentile in percentiles_sort:
                if len(percentiles[percentile].min) > 0:
                    suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                    table.add_column(f"Min{suffix}", percentiles[percentile].min[group])
            for percentile in percentiles_sort:
                if len(percentiles[percentile].max) > 0:
                    suffix = f" {int(percentile * 100)}ph" if percentile < 1 else ""
                    table.add_column(f"Max{suffix}", percentiles[percentile].max[group])

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

        return summary_table


