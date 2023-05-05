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

![graph](https://fivekg.onrender.com/images/qgate/PRF-NoSQL_igz_nonprod-2023-04-23_14-41-18-bulk-100x50.png)
![graph](https://fivekg.onrender.com/images/qgate/EXE-NoSQL-2023-05-04_19-33-30-bulk-1x50-plan-8x2.png)


