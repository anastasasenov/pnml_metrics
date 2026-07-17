# PNML Metrics

A simple tool for Petri Net metrics. It reads process models ( https://www.pnml.org ) and checks them for complexity, duplicate tasks, and hidden weaknesses.

## What it Measures

* Graph Density: How crowded or complex the network connections are.Behavioral ( https://wikipedia.org/wiki/Bipartite_graph )
* Entropy: How many unpredictable choice points exist in the process.Redundancy ( https://wikipedia.org/wiki/Entropy_(information_theory) )
* Ratio: The percentage of duplicate tasks (clones) in the system ( https://wikipedia.org/wiki/Petri_net )
* Single Points of Failure (SPOF): Strict bottlenecks where a single failure stops everything ( https://wikipedia.org/wiki/Single_point_of_failure )

## Architecture

PNML file -> XML parser -> Graph extraction -> Metric calculations -> JSON report

## Usage

```python
$> pnml_metrics.py PetriNet.pnml
{
    "file_name": "PetriNet.pnml",
     "structural_metrics": {
        "places": 2,
        "transitions": 1,
        "total_nodes": 3,
        "arcs": 2
    },
    "complexity_metrics": {
        "graph_structural_density": 0.5
    },
    "resilience_metrics": {
        "behavioral_structural_entropy_bits": 0.0,
        "structural_redundancy_ratio": 0.0,
        "duplicate_clusters": 0,
        "architecture_resilience_score": 100,
        "single_points_of_failure": []
    }
}
```

## License

This project is open-source and available under the MIT License. Feel free to modify and adapt it.
