import os.path, os
import matplotlib.axes
import matplotlib.pyplot as plt
import qgate_graph.file_format as const
import json, datetime
import logging
import numpy
from qgate_graph.graph_base import GraphBase

class GraphPerformance(GraphBase):
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
    def __init__(self, dpi=100):
        super().__init__(dpi)

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

    def _expected_round(self,avrg_time):

        avrg=numpy.average(avrg_time)
        zero_count=1    #   minimal number of zeros

        split=str(avrg).split('.')
        if len(split)>1:
            # calculation amount of zeros
            for c in split[1]:
                if c!='0':
                    break
                else:
                    zero_count=zero_count+1
        return zero_count

    def _show_graph(self, executors, total_performance, avrg_time, std_deviation, title, file_name, output_dir) -> str:
        plt.style.use("bmh") #"ggplot" "seaborn-v0_8-poster"
        fig, ax = plt.subplots(2, 1, sharex='none', squeeze=False, figsize=(15, 6))
        ax_main: matplotlib.axes.Axes = ax[0][0]

        # view total performance
        self._watermark(plt, ax_main)

        plt.suptitle("Performance & Response time",weight='bold', fontsize=18, ha="center", va="top")
        ax_main.set_title(title, fontsize=14, ha="center", va="top")
        self._reset_marker()
        self._reset_color()

        for key in executors.keys():
            ax_main.plot(executors[key], total_performance[key], color=self._next_color(), linestyle="-", marker=self._next_marker(), label=f"{key} [{round(max(total_performance[key]), 2)}]")

        if len(executors)>0:
            ax_main.legend()

        #ax_main.set_xlabel('Executors')
        ax_main.set_ylabel('Performance [calls/sec]')
        ax_main.set_xticks(self._get_executor_list(collections=executors))

        # remove duplicit axis (because matplotlib>=3.8)
        ax[1][0].remove()

        # draw detail graphs
        key_count=len(executors.keys())
        key_view=key_count
        self._reset_marker()
        self._reset_color()
        for key in executors.keys():
            # view response time
            key_view+=1
            ax=plt.subplot(2, key_count, key_view)
            ax.errorbar(executors[key], avrg_time[key], std_deviation[key], alpha=0.5,color=self._next_color(), ls='none', marker=self._next_marker(), linewidth=2, capsize=6)
            self._watermark(plt, ax)

            expected_round=self._expected_round(avrg_time[key])
            for x, y in zip(executors[key], avrg_time[key]):
                ax.annotate(round(y,expected_round),   # previous code plt.annotate(round(y,1),
                             (x,y),
                             textcoords="offset points",
                             xytext=(0,-2),
                             ha='center',
                             size=8,
                             weight='normal')           # previous code weight='bold'

            ax.set_xlabel('Executors')
            if key_count+1==key_view:
                ax.set_ylabel('Response [sec]')
            ax.set_xticks(self._get_executor_list(collection=executors[key]))
            ax.grid(visible=True)

        output_file=os.path.join(output_dir,file_name+".png")
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
        file_name=None
        total_performance={}
        avrg_time={}
        std_deviation={}
        executors={}
        output_list=[]

        logging.info(f"Processing '{input_file}' ...")

        # copy dir because the path can be modificated
        output_dir_target = output_dir

        # create output dir, if not exist
        if not os.path.exists(output_dir_target):
            os.makedirs(output_dir_target)

        with open(input_file, "r") as f:
            while True:
                line=f.readline()
                if not line:
                    break
                line=line.strip()
                if len(line)==0:
                    continue
                if line[0]=='#':
                    if file_name and len(executors)>0:
                        if suppress_error:
                            try:
                                output_list.append(
                                    self._show_graph(executors, total_performance, avrg_time, std_deviation,title,
                                                     file_name,output_dir_target))
                            except Exception as ex:
                                logging.info(f"  ... Error in '{file_name}', '{type(ex)}'")
                        else:
                            output_list.append(
                                self._show_graph(executors, total_performance, avrg_time, std_deviation, title,
                                                 file_name, output_dir_target))
                    file_name=None
                    executors.clear()
                    total_performance.clear()
                    avrg_time.clear()
                    std_deviation.clear()
                    continue
                input_dict=json.loads(line)
                if input_dict[const.FileFormat.PRF_TYPE]==const.FileFormat.PRF_HDR_TYPE:
                    # header
                    start_date = input_dict[const.FileFormat.PRF_HDR_NOW]
                    report_date=datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d %H-%M-%S")
                    label=input_dict[const.FileFormat.PRF_HDR_LABEL]
                    bulk=input_dict[const.FileFormat.PRF_HDR_BULK]
                    duration = input_dict.get(const.FileFormat.PRF_HDR_DURATION, -1)
                    if duration >= 0:
                        # update output dir based on duration (e.g. 1 min, 5 sec, etc.) and date
                        output_dir_target = os.path.join(output_dir,
                                                         self._readable_duration(duration),
                                                         datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d"))
                        # create subdirectory based on duration
                        if not os.path.exists(output_dir_target):
                            os.makedirs(output_dir_target)
                    file_name=self._unique_file_name("PRF", label, report_date, bulk)
                    title=f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}, duration '{self._readable_duration(duration)}'"

                elif input_dict[const.FileFormat.PRF_TYPE]==const.FileFormat.PRF_CORE_TYPE:
                    # core
                    if input_dict[const.FileFormat.PRF_CORE_GROUP] in executors:
                        executors[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(input_dict[const.FileFormat.PRF_CORE_REAL_EXECUTOR])
                        total_performance[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(input_dict[const.FileFormat.PRF_CORE_TOTAL_CALL_PER_SEC])
                        avrg_time[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(input_dict[const.FileFormat.PRF_CORE_AVRG_TIME])
                        std_deviation[input_dict[const.FileFormat.PRF_CORE_GROUP]].append(input_dict[const.FileFormat.PRF_CORE_STD_DEVIATION])
                    else:
                        executors[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [input_dict[const.FileFormat.PRF_CORE_REAL_EXECUTOR]]
                        total_performance[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [input_dict[const.FileFormat.PRF_CORE_TOTAL_CALL_PER_SEC]]
                        avrg_time[input_dict[const.FileFormat.PRF_CORE_GROUP]] = [input_dict[const.FileFormat.PRF_CORE_AVRG_TIME]]
                        std_deviation[input_dict[const.FileFormat.PRF_CORE_GROUP]]=[input_dict[const.FileFormat.PRF_CORE_STD_DEVIATION]]
        return output_list