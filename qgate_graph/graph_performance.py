from matplotlib import axes
from matplotlib import pyplot as plt
from qgate_graph.file_format import FileFormat as const
from numpy import std, average
from qgate_graph.graph_base import GraphBase
from qgate_graph.percentile_item import PercentileItem
from qgate_graph.circle_queue import CircleQueue, ColorQueue, MarkerQueue
import os.path, os
import datetime
import logging


class GraphPerformance(GraphBase):
    MIN_PRECISION = 0
    MAX_PRECISION = 4
    MAX_PRECISION_FORMAT = "{num:.4f}"

    """
    Generate graph based on input data

        example::

            import qgate_graph.graph_performance as grp
            import logging

            logging.basicConfig()
            logging.getLogger().setLevel(logging.INFO)

            graph=grp.GraphPerformance()
            graph.generate_from_dir("input_adr", "output_adr")
    """
    def __init__(self, dpi = 100, min_precision = -1, max_precision = -1, raw_format = False):
        super().__init__(dpi)
        self._min_precision = min_precision if min_precision >= 0 else GraphPerformance.MIN_PRECISION
        self._max_precision = max_precision if max_precision >= 0 else GraphPerformance.MAX_PRECISION
        self._max_precision_format = "{num:." + str(self._max_precision) + "f}"
        self._raw_format = raw_format

    def _get_executor_list(self, collections=None, collection=None):
        """
        Get list of executor for graph X-line
        :param collections:
        :param collection:
        :return:
        """
        list=[]
        if collections:
            for key in collections.keys():
                for executor in collections[key]:
                    if executor not in list:
                        list.append(executor)
        else:
            if collection:
                for executor in collection:
                    if executor not in list:
                        list.append(executor)
        return list

    def _expected_round(self, avrg_time):
        """Calculation amount of precisions for number presentation"""

        # calc max by number precision
        max_len = 0
        min_zero = self._max_precision
        max_zero = self._min_precision
        for a in avrg_time:
            split = self._max_precision_format.format(num=a).split('.')

            if len(split)>1:
                decimal_item = split[1].rstrip('0')
                size = len(decimal_item)
                if size > max_len:
                    max_len = size

                zero_prefix = 0
                skip = True
                for c in decimal_item:
                    zero_prefix += 1
                    if c != '0':
                        skip = False
                        break

                if not skip:
                    min_zero = min(zero_prefix, min_zero)
                    max_zero = max(zero_prefix, max_zero)
        if max_len == 0:
            return self._min_precision

        # max by standard deviation
        deviation = std(avrg_time)
        if deviation > 1:
            return int(average([min_zero,max_zero]))
        else:
            max_stddev = 0
            limit = False
            split = self._max_precision_format.format(num=deviation).split('.')
            if len(split) > 1:
                # calculation amount of zeros
                for c in split[1]:
                    max_stddev += 1
                    if c != '0':
                        limit = True
                        break

            if max_stddev>max_len:
                max_stddev=max_len

            if limit:
                return max_stddev if max_stddev > max_zero else max_zero
            return max_len

    def _create_output(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        return self._create_graph(percentiles, title, f"PRF{file_name}.png", output_dir)

    def _create_graph(self, percentiles: {PercentileItem}, title, file_name, output_dir) -> str:
        alpha = CircleQueue([0.4, 0.8] if len(percentiles) > 1 else [0.8])
        line_style = CircleQueue(['--','-'] if len(percentiles) > 1 else ['-'])
        color = ColorQueue()
        marker = MarkerQueue()
        plt.style.use("bmh") #"ggplot" "seaborn-v0_8-poster"
        fig, ax = plt.subplots(2, 1, sharex='none', squeeze=False, figsize=(15, 6))
        ax_main: axes.Axes = ax[0][0]

        # view total performance
        self._watermark(plt, ax_main)

        plt.suptitle("Performance & Response time",weight='bold', fontsize=18, ha="center", va="top")
        ax_main.set_title(title, fontsize=14, ha="center", va="top")

        # plot main graph 'Performance [calls/second]' (plus amount of executors)
        for percentile in percentiles.values():
            for key in percentile.executors.keys():
                ax_main.plot(percentile.executors[key], percentile.total_performance[key],
                             color = color.next(),
                             linestyle = line_style.item(),
                             marker = marker.next(),
                             alpha = alpha.item(),
                             label = f"{key} "
                                     f"{str(int(percentile.percentile*100))+'ph ' if percentile.percentile != 1 else ''}"
                                     f"[{round(max(percentile.total_performance[key]), 2):,}]")

            marker.reset()
            color.reset()
            alpha.next()
            line_style.next()

        if len(percentiles[1].executors) > 0:
            ax_main.legend(fontsize = 'small')

        ax_main.set_ylabel('Performance [calls/sec]')
        ax_main.set_xticks(self._get_executor_list(collections=percentiles[1].executors))

        # remove duplicit axis (because matplotlib>=3.8)
        ax[1][0].remove()

        # draw detail graphs 'Response time [seconds]'
        key_count = len(percentiles[1].executors)
        key_view = key_count
        marker.reset()
        color.reset()
        alpha.reset()
        for key in percentiles[1].executors.keys():
            # view response time
            key_view += 1
            ax=plt.subplot(2, key_count, key_view)

            for percentile in percentiles.values():
                ax.errorbar(percentile.executors[key], percentile.avrg_time[key], percentile.std_deviation[key],
                            alpha = alpha.next(),
                            color = color.item(),
                            linestyle = 'none', #'-' if (len(percentiles) > 1 and percentile.percentile != 1) or (len(percentiles) == 1) else 'none',
                            marker = '_' if (len(percentiles) > 1 and percentile.percentile != 1) or (len(percentiles) == 1) else 'none',
                            linewidth = 2 if (len(percentiles) > 1 and percentile.percentile != 1) or (len(percentiles) == 1) else 1,
                            capsize = 6 if (len(percentiles) > 1 and percentile.percentile != 1) or (len(percentiles) == 1) else 6)
                self._watermark(plt, ax)
                ax.legend(['avrg ± std', f"avrg ± std {str(int(percentile.percentile*100))+'ph ' if percentile.percentile != 1 else ''}"],
                          fontsize = 'small')

                # add table
                # val1 = ["{:X}".format(i) for i in range(10)]
                # val2 = ["{:02X}".format(10 * i) for i in range(10)]
                # val3 = [["" for c in range(10)] for r in range(10)]
                # table = ax.table(
                #     cellText=val3,
                #     rowLabels=val2,
                #     colLabels=val1,
                #     rowColours=["palegreen"] * 10,
                #     colColours=["palegreen"] * 10,
                #     cellLoc='center',
                #     loc='upper left')

                # add Y-lines
                # if percentile.percentile != 1:
                #     lim = ax.get_ylim()
                #     ax.set_yticks(list(ax.get_yticks()) + percentile.avrg_time[key])
                #     ax.set_ylim(lim)

                # get size of Y-axes
                #print(ax.get_yticks())

                # print response time value with relevant precision
                if (len(percentiles) > 1 and percentile.percentile != 1) or (len(percentiles) == 1):
                    expected_round = self._expected_round(percentile.avrg_time[key])
                    for x, y in zip(percentile.executors[key], percentile.avrg_time[key]):
                        ax.annotate(round(y,expected_round),
                                    (x,y),
                                    textcoords = "offset fontsize",
                                    xytext = (0,0),
                                    ha = 'center', #'center',
                                    va = 'center', #'center',
                                    size = 9,
                                    weight = 'normal')
                                    #annotation_clip = True)           # previous code weight='bold'

                ax.set_xlabel('Executors')
                if key_count+1 == key_view:
                    ax.set_ylabel('Response [sec]')
                ax.set_xticks(self._get_executor_list(collection=percentile.executors[key]))
                ax.grid(visible = True)
            color.next()
            marker.next()

        output_file = os.path.join(output_dir, file_name)
        plt.savefig(output_file, dpi=self.dpi)
        logging.info(f"  ... {output_file}")
        plt.close()
        return output_file

    def generate_from_dir(self, input_dir: str="input", output_dir: str="output") -> list[str]:
        """
        Generate graphs based on input directory

        example::

            import qgate_graph.graph_performance as grp

            graph=grp.GraphPerformance()
            graph.generate_from_dir("input_adr", "output_adr")

        :param input_dir:       Input directory (default "input")
        :param output_dir:      Output directory (default "output")
        :return:                List of generated files
        """
        output_list=[]

        for input_file in os.listdir(input_dir):
            for file in self.generate_from_file(os.path.join(input_dir, input_file), output_dir):
                output_list.append(file)
        logging.info("Done")
        return output_list

    def generate_from_file(self, input_file: str, output_dir: str="output", suppress_error = False) -> list[str]:
        """
        Generate graphs based on input file

        :param input_file:      Input file
        :param output_dir:      Output directory (default "output")
        :param suppress_error:  Ability to suppress error (default is False)
        :return:                List of generated files
        """
        file_name = None
        output_list = []
        percentiles = {}
        percentiles[1] = PercentileItem(1)

        logging.info(f"Processing '{input_file}' ...")

        # copy dir because the path can be modificated
        output_dir_target = output_dir

        # create output dir, if not exist
        if not os.path.exists(output_dir_target):
            os.makedirs(output_dir_target, mode = 0o777)

        with open(input_file, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == '#':
                    if file_name and len(percentiles[1].executors) > 0:
                        if suppress_error:
                            try:
                                output_list.append(self._create_output(percentiles, title, file_name, output_dir_target))
                            except Exception as ex:
                                logging.info(f"  ... Error in '{file_name}', '{type(ex)}'")
                        else:
                            output_list.append(self._create_output(percentiles, title, file_name, output_dir_target))
                    file_name = None
                    percentiles.clear()
                    percentiles[1] = PercentileItem(1)
                    continue
                input_dict = GraphBase.load_json(line)
                if not input_dict:
                    continue
                if input_dict[const.PRF_TYPE] == const.PRF_HDR_TYPE:
                    # header items
                    start_date = input_dict[const.PRF_HDR_NOW]
                    report_date = datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d %H-%M-%S")
                    label = input_dict[const.PRF_HDR_LABEL]
                    bulk = input_dict[const.PRF_HDR_BULK]
                    duration = input_dict.get(const.PRF_HDR_DURATION, -1)
                    if duration >= 0:
                        # update output dir based on duration (e.g. 1 min, 5 sec, etc.) and date
                        output_dir_target = os.path.join(output_dir,
                                                         self._readable_duration(duration),
                                                         datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d"))
                        # create subdirectory based on duration
                        if not os.path.exists(output_dir_target):
                            os.makedirs(output_dir_target, mode=0o777)
                    # add percentile
                    if input_dict.get(const.PRF_HDR_PERCENTILE, 1) < 1:
                        percentiles[input_dict[const.PRF_HDR_PERCENTILE]] = PercentileItem(input_dict[const.PRF_HDR_PERCENTILE])
                    file_name = self._unique_file_name("", label, report_date, bulk, self._raw_format)
                    title = f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}, duration '{self._readable_duration(duration)}'"

                elif input_dict[const.PRF_TYPE] == const.PRF_CORE_TYPE:

                    for percentile_key in percentiles.keys():
                        suffix = f"_{int(percentile_key * 100)}" if percentile_key < 1 else ""
                        group = input_dict[const.PRF_CORE_GROUP]# if percentile == 1 else f"{input_dict[const.PRF_CORE_GROUP]}, {int(percentile * 100)}ph"
                        percentile = percentiles[percentile_key]

                        # core items
                        if group in percentile.executors:
                            percentile.executors[group].append(input_dict[const.PRF_CORE_REAL_EXECUTOR])
                            if self._raw_format:
                                total_calls_sec_raw = input_dict.get(const.PRF_CORE_TOTAL_CALL_PER_SEC_RAW + suffix, None)
                                if total_calls_sec_raw is None:
                                    total_calls_sec_raw = input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC + suffix] / bulk[0]
                                percentile.total_performance[group].append(total_calls_sec_raw)
                            else:
                                percentile.total_performance[group].append(input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC + suffix])
                            percentile.avrg_time[group].append(input_dict[const.PRF_CORE_AVRG_TIME + suffix])
                            percentile.std_deviation[group].append(input_dict[const.PRF_CORE_STD_DEVIATION + suffix])
                            if input_dict.get(const.PRF_CORE_MIN + suffix, None):
                                percentile.min[group].append(input_dict[const.PRF_CORE_MIN + suffix])
                            if input_dict.get(const.PRF_CORE_MAX + suffix, None):
                                percentile.max[group].append(input_dict[const.PRF_CORE_MAX + suffix])
                        else:
                            percentile.executors[group] = [input_dict[const.PRF_CORE_REAL_EXECUTOR]]
                            if self._raw_format:
                                total_calls_sec_raw = input_dict.get(const.PRF_CORE_TOTAL_CALL_PER_SEC_RAW + suffix, None)
                                if total_calls_sec_raw is None:
                                    total_calls_sec_raw = input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC + suffix] / bulk[0]
                                percentile.total_performance[group] = [total_calls_sec_raw]
                            else:
                                percentile.total_performance[group] = [input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC + suffix]]
                            percentile.avrg_time[group] = [input_dict[const.PRF_CORE_AVRG_TIME + suffix]]
                            percentile.std_deviation[group] = [input_dict[const.PRF_CORE_STD_DEVIATION + suffix]]
                            if input_dict.get(const.PRF_CORE_MIN + suffix, None):
                                percentile.min[group] = [input_dict[const.PRF_CORE_MIN + suffix]]
                            if input_dict.get(const.PRF_CORE_MAX + suffix, None):
                                percentile.max[group] = [input_dict[const.PRF_CORE_MAX + suffix]]
        return output_list


