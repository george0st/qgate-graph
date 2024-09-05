import os.path, os
import matplotlib.pyplot as plt
import qgate_graph.file_format as const
from qgate_graph.graph_base import GraphBase
import json, datetime
import logging

class GraphExecutor(GraphBase):
    """
    Generate graph based on input data

        example::

            import qgate_graph.graph_executor as grp
            import logging

            logging.basicConfig()
            logging.getLogger().setLevel(logging.INFO)

            graph=grp.GraphExecutor()
            graph.generate_from_dir("input_adr", "output_adr")
    """
    def __init__(self, dpi=100):
        super().__init__(dpi)

    def generate_from_dir(self, input_dir: str = "input", output_dir: str = "output") -> list[str]:
        """
        Generate graphs about executors in time based on input directory

        example::

            import qgate_graph.graph as grp

            graph=grp.Graph()
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

    def _order(self, date_arr: list):
        date_arr.sort(key=lambda x: x[0])

    def _add_counter2(self, itm, new_array, new_array_count):

        if itm:
            for j in range(len(itm)):
                new_item=datetime.datetime.fromisoformat(itm[j]).replace(microsecond=0)

                found = False
                for i in new_array:
                    if i[0] == new_item:
                        if j==1:
                            i[1]=i[1]+1
                        elif j==2:
                            i[1] = i[1] - 1
                        found = True
                        break
                if found == False:
                    if j==0:
                        new_array.append([new_item, 0])
                    elif j==1:
                        new_array.append([new_item, 1])
                    elif j==2:
                        new_array.append([new_item, -1])

    def generate_from_file(self, input_file: str, output_dir: str = "output", suppress_error = False) -> list[str]:
        """
        Generate graphs about executors based on input file

        :param input_file:      Input file
        :param output_dir:      Output directory (default "output")
        :param suppress_error:  Ability to suppress error (default is False)
        :return:                List of generated files
        """
        file_name = None
        executors = {}
        executor = []
        input_dict = {}
        end_date = None
        start_date = None
        output_list = []

        logging.info(f"Processing '{input_file}' ...")

        # copy dir because the path can be modificated
        output_dir_target = output_dir

        # create output dir if not exist
        if not os.path.exists(output_dir_target):
            os.makedirs(output_dir_target)

        with open(input_file, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line[0] == '#':
                    file_name = None
                    executors.clear()
                    executor.clear()
                    continue
                input_dict = GraphBase.load_json(line)
                if not input_dict:
                    continue
                if input_dict[const.FileFormat.PRF_TYPE] == const.FileFormat.PRF_HDR_TYPE:
                    # header
                    start_date=input_dict[const.FileFormat.PRF_HDR_NOW]
                    report_date = datetime.datetime.fromisoformat(start_date).strftime(
                        "%Y-%m-%d %H-%M-%S")
                    label = input_dict[const.FileFormat.PRF_HDR_LABEL]
                    bulk = input_dict[const.FileFormat.PRF_HDR_BULK]
                    duration = input_dict.get(const.FileFormat.PRF_HDR_DURATION, -1)
                    if duration >= 0:
                        # update output dir based on duration (e.g. 1 min, 5 sec, etc.) and date
                        output_dir_target = os.path.join(output_dir,
                                                         self._readable_duration(duration),
                                                         datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d"))
                        # create subdirectory based on duration
                        if not os.path.exists(output_dir_target):
                            os.makedirs(output_dir_target)
                    bulk_name=f"{bulk[0]}/{bulk[1]}"
                    file_name = self._unique_file_name("EXE", label, report_date, bulk)
                    title = f"'{label}', {report_date}, bulk {bulk[0]}/{bulk[1]}, duration '{self._readable_duration(duration)}'"

                elif input_dict[const.FileFormat.PRF_TYPE] == const.FileFormat.PRF_CORE_TYPE:
                    # core
                    # executors[input_dict[const.FileFormat.PRF_CORE_PLAN_EXECUTOR]].append(
                    #     input_dict[const.FileFormat.PRF_CORE_TIME_END])

                    if executor:
                        plan=f"{input_dict[const.FileFormat.PRF_CORE_PLAN_EXECUTOR][0]}x{input_dict[const.FileFormat.PRF_CORE_PLAN_EXECUTOR][1]}"
                        executors[plan]=executor

                        if input_dict.get(const.FileFormat.PRF_CORE_TIME_END):
                            end_date=input_dict[const.FileFormat.PRF_CORE_TIME_END]

                        #file_name=f"{file_name}-plan-{plan}"
                        if suppress_error:
                            try:
                                output_list.append(
                                    self._show_graph(start_date, executors, end_date, title, f"{file_name}-plan-{plan}",
                                                     output_dir_target))
                            except Exception as ex:
                                logging.info(f"  ... Error in '{file_name}-plan-{plan}', '{type(ex)}'")
                        else:
                            output_list.append(
                                self._show_graph(start_date, executors, end_date, title, f"{file_name}-plan-{plan}",
                                                 output_dir_target))

                        executors.clear()
                        executor.clear()
                elif input_dict[const.FileFormat.PRF_TYPE] == const.FileFormat.PRF_DETAIL_TYPE:
                    # detail
                    if not input_dict.get(const.FileFormat.PRF_DETAIL_ERR):
                        executor.append([
                            input_dict[const.FileFormat.PRF_DETAIL_TIME_INIT],
                            input_dict[const.FileFormat.PRF_DETAIL_TIME_START],
                            input_dict[const.FileFormat.PRF_DETAIL_TIME_END]])
        return output_list

    def _show_graph(self, start_date, executors, end_date, title, file_name, output_dir) -> str :
        plt.style.use("bmh") #"ggplot" "seaborn-v0_8-poster"
        ax=plt.figure(figsize=(15, 6))
        plt.grid()

        # osa X = end_date - start_date
        # osa Y = current executions

        # view total performance
        ax=plt.subplot(1,1,1)
        self._watermark(plt,ax)

        plt.suptitle("Executors in time",weight='bold', fontsize=18, ha="center", va="top")
        plt.title(title, fontsize=14,ha="center", va="top")
        self._reset_marker()
        self._reset_color(6)

        new_array=[]
        new_array_count=[]

        # group values
        for key in executors.keys():
            for itm in executors[key]:
                self._add_counter2(itm, new_array, new_array_count)


        # add start
#        new_array.insert(0, [datetime.datetime.fromisoformat(start_date).replace(microsecond=0),0])

        # add end
#        new_array.append([datetime.datetime.fromisoformat(end_date).replace(microsecond=0),0])

        # order
        self._order(new_array)

        # recalc (+/- values)
        for i in range(len(new_array)):
            if i==0:
                count=new_array[i][1]
            else:
                count+=new_array[i][1]
                new_array[i][1]=count

        # transform
        new_array2=[]
        for i in new_array:
            new_array_count.append(i[1])
            new_array2.append(i[0])

        for key in executors.keys():
            plt.step(new_array2,new_array_count,where='post',
                  color=self._next_color(), linestyle="-", marker=self._next_marker(), label=f"{key}")

        output_file=os.path.join(output_dir,file_name+".png")
        plt.savefig(output_file, dpi=self.dpi)
        logging.info(f"  ... {output_file}")
        plt.close()
        return output_file


