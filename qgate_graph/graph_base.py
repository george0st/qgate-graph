import os.path, os
import matplotlib.pyplot as plt
import qgate_graph.file_format as const
import qgate_graph
import json, datetime
import logging

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
        self._colors=['c', 'm', 'r', 'b', 'g', 'y', 'k', 'w']
        self._reset_color()
        self.dpi=dpi

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

    def _reset_color(self):
        self._color_point=0

    def _watermark(self, plt, ax):
        """
        Add watermark to the graph
        :param plt:
        :param ax:
        """
        watermark=f'qgate_graph (v{qgate_graph.__version__})'
        plt.text(1.0, 0, watermark,
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 transform = ax.transAxes,
                 alpha=0.4, fontsize=8)

    def _unife_file_name(self, prefix, label, report_date, bulk):
        """
        Generate unique name based on key information

        :param prefix:      Optional name
        :param label:       Label (typically from perf test)
        :param report_date: Report date
        :param bulk:        Bulk (rows, columns) size
        :return:            Return relevant name
        """
        file_name=f"{prefix}-{label}-{report_date}-bulk-{bulk[0]}x{bulk[1]}"
        remove_item=" ,&?"
        for itm in remove_item:
            file_name=file_name.replace(itm,"_")
        file_name=file_name.replace("__","_")
        return file_name