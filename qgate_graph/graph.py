import os.path, os
import matplotlib.pyplot as plt
import qgate_graph.constant as cns
import json, datetime
import logging
class Graph:
    def __init__(self):
        self._markers = ['o','x', '*', '^','X', 'D', 'p', 'H']
        self._marker_point=0
        self._colors=['c', 'm', 'r', 'b', 'g', 'y', 'k', 'w']
        self._color_point=0

    def _find_key(self, performance_line: str, keys):
        for key in keys:
            start=performance_line.index(key)
            if start>0:
                start+=len(key)
                end = performance_line.index(",",start)
                val=performance_line[start:end]
                return val.strip()
        return None

    def _get_executor_list(self, collections=None, collection=None):
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

    def _next_marker(self):
        self._marker_point = self._marker_point + 1
        if self._marker_point >= len(self._markers):
            self._marker_point=0

    def _next_color(self):
        self._color_point = self._color_point + 1
        if self._color_point >= len(self._colors):
            self._color_point=0

    def _get_marker(self):
        return self._markers[self._marker_point]

    def _get_color(self):
        return self._colors[self._color_point]

    def _reset_marker(self):
        self._marker_point=0

    def _reset_color(self):
        self._color_point=0

    def _watermark(self, plt, ax):
        watermark='qgate_graph (v1.1)'
        plt.text(1.0, 0, watermark,
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 transform = ax.transAxes,
                 alpha=0.4, fontsize=8)

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
            plt.plot(executors[key], total_performance[key], color=self._get_color(), linestyle="-", marker=self._get_marker(), label=f"{key} [{round(max(total_performance[key]),2)}]")
            self._next_marker()
            self._next_color()


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
            plt.errorbar(executors[key], avrg_time[key], std_deviation[key], alpha=0.5,color=self._get_color(), ls='none', marker=self._get_marker(), linewidth=2, capsize=6)
            self._watermark(plt, ax)

            for x, y in zip(executors[key], avrg_time[key]):
                plt.annotate(round(y,1),
                             (x,y),
                             textcoords="offset points",
                             xytext=(0,-2),
                             ha='center',
                             size=8,
                             weight='bold')

            self._next_marker()
            self._next_color()
            plt.xlabel('Executors')
            if key_count+1==key_view:
                plt.ylabel('Response [sec]')
            plt.xticks(self._get_executor_list(collection=executors[key]))

        output_file=os.path.join(output_dir,file_name+".png")
        plt.savefig(output_file, dpi=200)
        logging.info(f"  ... {output_file}")
        plt.close()

    def _unife_file_name(self, file_name):
        remove_item=" ,&?"
        for itm in remove_item:
            file_name=file_name.replace(itm,"_")
        file_name=file_name.replace("__","_")
        return file_name

    def generate_from_dir(self, input_dir: str="input", output_dir: str="output"):
        """
        Generate graphs based on input directory

        :param input_dir:       Input directory (default "input")
        :param output_dir:      Output directory (default "output")
        """
        for file in os.listdir(input_dir):
            self.generate_from_file(os.path.join(input_dir, file), output_dir)

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
                if input_dict[cns.Vocabulary.PRF_TYPE]==cns.Vocabulary.PRF_HDR_TYPE:
                    # header
                    report_date=datetime.datetime.fromisoformat(input_dict[cns.Vocabulary.PRF_HDR_NOW]).strftime("%Y-%m-%d %H-%M-%S")
                    label=input_dict[cns.Vocabulary.PRF_HDR_LABEL]
                    bulk=input_dict[cns.Vocabulary.PRF_HDR_BULK]
                    file_name=self._unife_file_name(f"{label}-{report_date}-bulk-{bulk[0]}x{bulk[1]}")
                    title=f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}"

                elif input_dict[cns.Vocabulary.PRF_TYPE]==cns.Vocabulary.PRF_CORE_TYPE:
                    # core
                    if input_dict[cns.Vocabulary.PRF_CORE_GROUP] in executors:
                        executors[input_dict[cns.Vocabulary.PRF_CORE_GROUP]].append(input_dict[cns.Vocabulary.PRF_CORE_REAL_EXECUTOR])
                        total_performance[input_dict[cns.Vocabulary.PRF_CORE_GROUP]].append(input_dict[cns.Vocabulary.PRF_CORE_TOTAL_CALL_PER_SEC])
                        avrg_time[input_dict[cns.Vocabulary.PRF_CORE_GROUP]].append(input_dict[cns.Vocabulary.PRF_CORE_AVRG_TIME])
                        std_deviation[input_dict[cns.Vocabulary.PRF_CORE_GROUP]].append(input_dict[cns.Vocabulary.PRF_CORE_STD_DEVIATION])
                    else:
                        executors[input_dict[cns.Vocabulary.PRF_CORE_GROUP]] = [input_dict[cns.Vocabulary.PRF_CORE_REAL_EXECUTOR]]
                        total_performance[input_dict[cns.Vocabulary.PRF_CORE_GROUP]] = [input_dict[cns.Vocabulary.PRF_CORE_TOTAL_CALL_PER_SEC]]
                        avrg_time[input_dict[cns.Vocabulary.PRF_CORE_GROUP]] = [input_dict[cns.Vocabulary.PRF_CORE_AVRG_TIME]]
                        std_deviation[input_dict[cns.Vocabulary.PRF_CORE_GROUP]]=[input_dict[cns.Vocabulary.PRF_CORE_STD_DEVIATION]]
