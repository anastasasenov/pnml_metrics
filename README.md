# PNML Metrics

A simple tool for Petri Net metrics. It reads process models ( https://www.pnml.org ) and checks them for complexity, duplicate tasks, and hidden weaknesses.

## What it Measures

* Graph Density: How crowded or complex the network connections are.Behavioral ( https://wikipedia.org/wiki/Bipartite_graph )
* Entropy: How many unpredictable choice points exist in the process.Redundancy ( https://wikipedia.org/wiki/Entropy_(information_theory) )
* Ratio: The percentage of duplicate tasks (clones) in the system ( https://wikipedia.org/wiki/Petri_net )

## Architecture

PNML file -> XML parser -> Graph extraction -> Metric calculations -> JSON report

## Usage

```python
$> pnml_metrics.py PetriNet.pnml
{
    "file_name": "PetriNet.pnml",
    "structural_metrics": {
        "places": 23,
        "transitions": 76,
        "total_nodes": 99,
        "arcs": 156
    },
    "complexity_metrics": {
        "graph_structural_density": 0.04462
    },
    "resilience_metrics": {
        "total_split_arcs": 67,
        "average_split_degree": 6.09091,
        "behavioral_structural_entropy": 15.55459,
        "structural_redundancy_ratio": 11.34211,
        "duplicate_clusters": 862,
        "resilience_score": 0.95652,
        "critical_places": [
            "p_8"
        ]
}
```

## License

This project is open-source and available under the MIT License. Feel free to modify and adapt it.
