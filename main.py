from qgate_graph.graph_performance import GraphPerformance
from qgate_graph.graph_executor import GraphExecutor
import qgate_graph
import click
import logging

@click.command()
@click.option("--input", help="input directory (default is directory 'input'", default="input")
@click.option("--output", help="output directory (default is directory 'output'", default="output")
def graph(input,output):
    """Generate graphs based in input data."""
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

#    graph=GraphPerformance()
#    graph.generate_from_dir(input, output)
    graph=GraphExecutor()
    graph.generate_from_file("input/prf_count_01.txt", output)
#    graph.generate_from_file("input/prf_nonprod_BDP_NoSQL.txt", output)


if __name__ == '__main__':
    graph()