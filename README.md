[![PyPI version fury.io](https://badge.fury.io/py/qgate-graph.svg)](https://pypi.python.org/pypi/qgate-graph/)
# QGate-Graph

Generate graphs based on performance outputs from Quality Gate solution.

## Usage

```lang-python
    from qgate_graph.graph_performance import GraphPerformance
    from qgate_graph.graph_executor import GraphExecutor
    import logging

    # setup login level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # generate performance/throughput graphs
    graph=GraphPerformance()
    graph.generate_from_dir()
    
    # generate excutors in time graphs
    graph=grp.GraphExecutor()
    graph.generate_from_dir()
```

# Outputs
![graph](./assets/NoSQL_bdp_nonprod-2023-04-22_17-08-34-bulk-10000x50.png)

