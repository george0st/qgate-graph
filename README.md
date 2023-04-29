[![PyPI version fury.io](https://badge.fury.io/py/qgate-graph.svg)](https://pypi.python.org/pypi/qgate-graph/)
# QGate-Graph

Generate graphs based on performance outputs from Quality Gate solution.

## Usage

    import qgate_graph.graph as grp
    import logging

    # setup login level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # generate output graphs
    graph=grp.Graph()
    graph.generate_from_dir()

# Outputs
![graph](./assets/NoSQL_bdp_nonprod-2023-04-22_17-08-34-bulk-10000x50.png)

