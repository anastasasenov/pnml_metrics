#!/usr/bin/python3

#-------------
# PNML metrics
#-------------


import json
import math
import sys
import xml.etree.ElementTree as ET


def parse_pnml_file(file_path: str):
    """Parses PNML and returns graph"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: Failed to parse XML in file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)

    places = set()
    transitions = {}
    arcs = set()

    for net in root.findall('.//{*}net'):
        for page in net.findall('.//{*}page') or [net]:
            for p in page.findall('.//{*}place'):
                p_id = p.get('id')
                if p_id:
                    places.add(p_id)
            
            for t in page.findall('.//{*}transition'):
                t_id = t.get('id')
                if t_id:
                    name_tag = t.find('.//{*}name/{*}text')
                    t_name = name_tag.text.strip() if name_tag is not None and name_tag.text else t_id
                    transitions[t_id] = {"name": t_name, "in": set(), "out": set()}

            for a in page.findall('.//{*}arc'):
                src = a.get('source')
                tgt = a.get('target')
                if src and tgt:
                    arcs.add((src, tgt))

    for src, tgt in arcs:
        if tgt in transitions:
            transitions[tgt]["in"].add(src)
        if src in transitions:
            transitions[src]["out"].add(tgt)

    return places, transitions, arcs


def calculate_resilience_data(places, transitions):
    """ Computes Entropy, Ratios, SOF"""
    total_split_arcs = 0
    split_degrees = []
    
    for p in places:
        out_count = sum(1 for t in transitions.values() if p in t["in"])
        if out_count > 1:
            split_degrees.append(out_count)
            total_split_arcs += out_count
            
    entropy = 0.0
    for p in places:
        out_count = sum(1 for t in transitions.values() if p in t["in"])
        if out_count > 1:
            p_i = 1.0 / out_count
            place_entropy = -sum(p_i * math.log2(p_i) for _ in range(out_count))
            entropy += place_entropy

    identical_pairs = 0
    t_ids = list(transitions.keys())
    
    for i in range(len(t_ids)):
        for j in range(i + 1, len(t_ids)):
            t1, t2 = t_ids[i], t_ids[j]
            if transitions[t1]["in"] == transitions[t2]["in"] and transitions[t1]["out"] == transitions[t2]["out"]:
                identical_pairs += 1
                
    redundancy_ratio = (identical_pairs / len(transitions)) if len(transitions) > 0 else 0.0

    critical_places = []
    for p in places:
        in_flows = sum(1 for t in transitions.values() if p in t["out"])
        out_flows = sum(1 for t in transitions.values() if p in t["in"])
        if in_flows >= 2 and out_flows >= 2:
            critical_places.append(p)
            
    resilience_score = 100 - (len(critical_places) * 20)
    resilience_score = max(0, min(100, resilience_score))

    return {
        "behavioral_structural_entropy_bits": round(entropy, 4),
        "structural_redundancy_ratio": round(redundancy_ratio, 4),
        "duplicate_clusters": identical_pairs,
        "architecture_resilience_score": resilience_score,
        "single_points_of_failure": critical_places
    }

def main():
    if len(sys.argv) < 2:
        print("PNML metrics version 1.0\n  Usage: " + sys.argv[0] + " file.pnml")
        exit(1)

    places, transitions, arcs = parse_pnml_file(sys.argv[1])

    num_p = len(places)
    num_t = len(transitions)
    num_a = len(arcs)
    num_nodes = num_p + num_t
    density = num_a / (2 * num_p * num_t) if (num_p * num_t) > 0 else 0.0

    resilience_data = calculate_resilience_data(places, transitions)

    output_payload = {
        "file_name": sys.argv[1],
        "structural_metrics": {
            "places": num_p,
            "transitions": num_t,
            "total_nodes": num_nodes,
            "arcs": num_a
        },
        "complexity_metrics": {
            "graph_structural_density": round(density, 5)
        }
    }
    output_payload["resilience_metrics"] = resilience_data
    print(json.dumps(output_payload, indent=4))

if __name__ == "__main__":
    main()
