from qgate_graph import __version__ as version
from matplotlib import get_backend, use
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
        self._markers = ['o','x', '*', '^','X', 'D', 'p', 'H']
        self._reset_marker()
        self._colors=['c', 'm', 'r', 'b', 'g', 'y', 'k']
        self._reset_color()
        self.dpi=dpi

        # use 'Agg' as non-interactive backend for matplotlib
        if get_backend().lower()!="agg":
            use('Agg', force = True)

    def _next_marker(self):
        current=self._marker_point
        self._marker_point = self._marker_point+1 if (self._marker_point+1) < len(self._markers) else 0
        return self._markers[current]

    def _reset_marker(self):
        self._marker_point=0

    def _next_color(self):
        current=self._color_point
        self._color_point = self._color_point+1 if (self._color_point+1) < len(self._colors) else 0
        return self._colors[current]

    def _reset_color(self, color_point=0):
        self._color_point=color_point

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

    def _unique_file_name(self, prefix, label, report_date, bulk, raw_format = False):
        """
        Generate unique name based on key information

        :param prefix:      Optional name
        :param label:       Label (typically from perf test)
        :param report_date: Report date
        :param bulk:        Bulk (rows, columns) size
        :return:            Return relevant name
        """
        file_name=f"{prefix}-{label}{'-RAW' if raw_format else ''}-{report_date}-bulk-{bulk[0]}x{bulk[1]}"
        remove_item=" ,&?"
        for itm in remove_item:
            file_name=file_name.replace(itm,"_")
        file_name=file_name.replace("__","_")
        return file_name

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



