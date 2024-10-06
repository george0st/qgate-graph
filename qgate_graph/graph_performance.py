from matplotlib import axes
from matplotlib import pyplot as plt
from qgate_graph.file_format import FileFormat as const
from numpy import std, average
from qgate_graph.graph_base import GraphBase
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

    def _exp_size(self, i):
        return int("{:.5e}".format(i).split("e")[1]) + 1  # e.g. `1e10` -> `10` + 1 -> 11

    def mod_size(self, i):
        return len("%i" % i)  # Uses string modulo instead of str(i)

    def expected_round(self, avrg_time):
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

    def _show_graph(self, executors, total_performance, avrg_time, std_deviation, title, file_name, output_dir) -> str:
        plt.style.use("bmh") #"ggplot" "seaborn-v0_8-poster"
        fig, ax = plt.subplots(2, 1, sharex='none', squeeze=False, figsize=(15, 6))
        ax_main: axes.Axes = ax[0][0]

        # view total performance
        self._watermark(plt, ax_main)

        plt.suptitle("Performance & Response time",weight='bold', fontsize=18, ha="center", va="top")
        ax_main.set_title(title, fontsize=14, ha="center", va="top")
        self._reset_marker()
        self._reset_color()

        # plot main graph 'Performance [calls/second]' (plus amount of executors)
        for key in executors.keys():
            ax_main.plot(executors[key], total_performance[key],
                         color=self._next_color(), linestyle="-",
                         marker=self._next_marker(),
                         label=f"{key} [{round(max(total_performance[key]), 2)}]")

        if len(executors)>0:
            ax_main.legend()

        #ax_main.set_xlabel('Executors')
        ax_main.set_ylabel('Performance [calls/sec]')
        ax_main.set_xticks(self._get_executor_list(collections=executors))

        # remove duplicit axis (because matplotlib>=3.8)
        ax[1][0].remove()

        # draw detail graphs 'Response time [seconds]'
        key_count=len(executors.keys())
        key_view=key_count
        self._reset_marker()
        self._reset_color()
        for key in executors.keys():
            # view response time
            key_view+=1
            ax=plt.subplot(2, key_count, key_view)
            ax.errorbar(executors[key], avrg_time[key], std_deviation[key],
                        alpha = 0.5, color = self._next_color(),
                        ls = 'none', marker = self._next_marker(),
                        linewidth = 2, capsize = 6)
            self._watermark(plt, ax)

            # print response time value with relevant precision
            expected_round = self.expected_round(avrg_time[key])
            for x, y in zip(executors[key], avrg_time[key]):
                ax.annotate(round(y,expected_round),   # previous code plt.annotate(round(y,1),
                             (x,y),
                             textcoords="offset points",
                             xytext=(0,-2),
                             ha='center',
                             size=8,
                             weight='normal')           # previous code weight='bold'

            ax.set_xlabel('Executors')
            if key_count+1 == key_view:
                ax.set_ylabel('Response [sec]')
            ax.set_xticks(self._get_executor_list(collection=executors[key]))
            ax.grid(visible = True)

        output_file = os.path.join(output_dir, file_name + ".png")
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
        total_performance = {}
        avrg_time = {}
        std_deviation = {}
        executors = {}
        output_list = []

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
                    if file_name and len(executors) > 0:
                        if suppress_error:
                            try:
                                output_list.append(
                                    self._show_graph(executors, total_performance, avrg_time, std_deviation,
                                                     title, file_name, output_dir_target))
                            except Exception as ex:
                                logging.info(f"  ... Error in '{file_name}', '{type(ex)}'")
                        else:
                            output_list.append(
                                self._show_graph(executors, total_performance, avrg_time, std_deviation,
                                                 title, file_name, output_dir_target))
                    file_name = None
                    executors.clear()
                    total_performance.clear()
                    avrg_time.clear()
                    std_deviation.clear()
                    continue
                input_dict = GraphBase.load_json(line)
                if not input_dict:
                    continue
                if input_dict[const.PRF_TYPE] == const.PRF_HDR_TYPE:
                    # header
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
                    file_name = self._unique_file_name("PRF", label, report_date, bulk, self._raw_format)
                    title = f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}, duration '{self._readable_duration(duration)}'"

                elif input_dict[const.PRF_TYPE] == const.PRF_CORE_TYPE:
                    # core
                    if input_dict[const.PRF_CORE_GROUP] in executors:
                        executors[input_dict[const.PRF_CORE_GROUP]].append(input_dict[const.PRF_CORE_REAL_EXECUTOR])
                        if self._raw_format:
                            total_calls_sec_raw = input_dict.get(const.PRF_CORE_TOTAL_CALL_PER_SEC_RAW, None)
                            if total_calls_sec_raw is None:
                                total_calls_sec_raw = input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC] / bulk[0]
                            total_performance[input_dict[const.PRF_CORE_GROUP]].append(total_calls_sec_raw)
                        else:
                            total_performance[input_dict[const.PRF_CORE_GROUP]].append(input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC])
                        avrg_time[input_dict[const.PRF_CORE_GROUP]].append(input_dict[const.PRF_CORE_AVRG_TIME])
                        std_deviation[input_dict[const.PRF_CORE_GROUP]].append(input_dict[const.PRF_CORE_STD_DEVIATION])
                    else:
                        executors[input_dict[const.PRF_CORE_GROUP]] = [input_dict[const.PRF_CORE_REAL_EXECUTOR]]
                        if self._raw_format:
                            total_calls_sec_raw = input_dict.get(const.PRF_CORE_TOTAL_CALL_PER_SEC_RAW, None)
                            if total_calls_sec_raw is None:
                                total_calls_sec_raw = input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC] / bulk[0]
                            total_performance[input_dict[const.PRF_CORE_GROUP]] = [total_calls_sec_raw]
                        else:
                            total_performance[input_dict[const.PRF_CORE_GROUP]] = [input_dict[const.PRF_CORE_TOTAL_CALL_PER_SEC]]
                        avrg_time[input_dict[const.PRF_CORE_GROUP]] = [input_dict[const.PRF_CORE_AVRG_TIME]]
                        std_deviation[input_dict[const.PRF_CORE_GROUP]] = [input_dict[const.PRF_CORE_STD_DEVIATION]]
        return output_list