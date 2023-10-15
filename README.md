[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version fury.io](https://badge.fury.io/py/qgate-graph.svg)](https://pypi.python.org/pypi/qgate-graph/)
![coverage](https://github.com/george0st/qgate-graph/blob/main/coverage.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/george0st/qgate-graph)
![GitHub release](https://img.shields.io/github/v/release/george0st/qgate-graph)

# QGate-Graph

The QGate graph generates graphical outputs based on performance tests (QGate Perf). Key benefits:
 - provide graphs about Performance/Throughput and Response time (on typically client side)
 - provide graphs about Executors in time

These graphs only visualize outputs from performance tests, it is not replacement of
detail views from Grafana, Prometheus, etc. in detail of CPU, GPU, RAM, I/O etc. on side of testing system.

## Usage

```python
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
    graph=GraphExecutor()
    graph.generate_from_dir()
```

## Outputs
#### Performance/Throughput & Response time
![graph](https://fivekg.onrender.com/images/qgate/PRF-Calc-2023-05-06_18-22-19-bulk-1x10.png)
![graph](https://fivekg.onrender.com/images/qgate/PRF-NoSQL_igz_nonprod-2023-04-23_14-41-18-bulk-100x50.png)

#### Executors in time
![graph](https://fivekg.onrender.com/images/qgate/EXE-Calc-2023-05-06_18-22-19-bulk-1x10-plan-128x4.png)
![graph](https://fivekg.onrender.com/images/qgate/EXE-NoSQL-2023-05-04_19-33-30-bulk-1x50-plan-8x2.png)


