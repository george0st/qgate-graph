import os.path, os
import matplotlib.pyplot as plt
import qgate_graph.file_format as const
import json, datetime
import logging
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
            for executor in collection:
                if executor not in list:
                    list.append(executor)
        return list

    def _show_graph(self, executors, total_performance, avrg_time, std_deviation, title, file_name,output_dir):
        plt.style.use("bmh") #"ggplot" "seaborn-v0_8-poster"
        ax=plt.figure(figsize=(15, 6))
        plt.grid()

        # view total performance
        ax=plt.subplot(2,1,1)
        self._watermark(plt,ax)

        plt.suptitle("Performance & Response time",weight='bold', fontsize=18, ha="center", va="top")
        plt.title(title, fontsize=14,ha="center", va="top")
        self._reset_marker()
        self._reset_color()

        for key in executors.keys():
            plt.plot(executors[key], total_performance[key], color=self._next_color(), linestyle="-", marker=self._next_marker(), label=f"{key} [{round(max(total_performance[key]),2)}]")

        plt.legend()
        #plt.xlabel('Executors')
        plt.ylabel('Performance [calls/sec]')
        plt.xticks(self._get_executor_list(collections=executors))

        # draw detail graphs
        key_count=len(executors.keys())
        key_view=key_count
        self._reset_marker()
        self._reset_color()
        for key in executors.keys():
            # view response time
            key_view+=1
            ax=plt.subplot(2, key_count, key_view)
            plt.errorbar(executors[key], avrg_time[key], std_deviation[key], alpha=0.5,color=self._next_color(), ls='none', marker=self._next_marker(), linewidth=2, capsize=6)
            self._watermark(plt, ax)

            for x, y in zip(executors[key], avrg_time[key]):
                plt.annotate(round(y,1),
                             (x,y),
                             textcoords="offset points",
                             xytext=(0,-2),
                             ha='center',
                             size=8,
                             weight='bold')

            plt.xlabel('Executors')
            if key_count+1==key_view:
                plt.ylabel('Response [sec]')
            plt.xticks(self._get_executor_list(collection=executors[key]))

        output_file=os.path.join(output_dir,file_name+".png")
        plt.savefig(output_file, dpi=self.dpi)
        logging.info(f"  ... {output_file}")
        plt.close()


    def generate_from_dir(self, input_dir: str="input", output_dir: str="output"):
        """
        Generate graphs based on input directory

        example::

            import qgate_graph.graph_performance as grp

            graph=grp.GraphPerformance()
            graph.generate_from_dir("input_adr", "output_adr")

        :param input_dir:       Input directory (default "input")
        :param output_dir:      Output directory (default "output")
        """
        for file in os.listdir(input_dir):
            self.generate_from_file(os.path.join(input_dir, file), output_dir)
        logging.info("Done")

    def generate_from_file(self, input_file: str, output_dir: str="output"):
        """
        Generate graphs based on input input file

        :param input_file:      Input file
        :param output_dir:      Output directory (default "output")
        """
        file_name=None
        total_performance={}
        avrg_time={}
        std_deviation={}
        executors={}

        logging.info(f"Processing '{input_file}' ...")
        with open(input_file, "r") as f:
            while True:
                line=f.readline()
                if not line:
                    break
                if line[0]=='#':
                    if file_name:
                        self._show_graph(executors, total_performance, avrg_time, std_deviation,title, file_name,output_dir)
                    file_name=None
                    executors.clear()
                    total_performance.clear()
                    avrg_time.clear()
                    std_deviation.clear()
                    continue
                input_dict=json.loads(line)
                if input_dict[const.FileFormat.PRF_TYPE]==const.FileFormat.PRF_HDR_TYPE:
                    # header
                    report_date=datetime.datetime.fromisoformat(input_dict[const.FileFormat.PRF_HDR_NOW]).strftime("%Y-%m-%d %H-%M-%S")
                    label=input_dict[const.FileFormat.PRF_HDR_LABEL]
                    bulk=input_dict[const.FileFormat.PRF_HDR_BULK]
                    file_name=self._unife_file_name("PRF",label,report_date,bulk)
                    title=f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}"

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