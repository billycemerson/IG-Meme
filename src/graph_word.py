from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import re

# Network Creation Functions

def create_word_network(word_pairs, min_frequency=1):
    """
    Create a directed word-to-word network.
    """
    G = nx.DiGraph()

    filtered_pairs = [(pair, freq) for pair, freq in word_pairs if freq >= min_frequency]

    for (w1, w2), freq in filtered_pairs:
        G.add_edge(w1, w2, weight=freq)

    return G, filtered_pairs


def create_word_emoji_network(word_emoji_pairs, min_frequency=1):
    """
    Create a directed word-to-emoji network.
    """
    G = nx.DiGraph()

    filtered_pairs = [(pair, freq) for pair, freq in word_emoji_pairs if freq >= min_frequency]

    for (w, e), freq in filtered_pairs:
        G.add_edge(w, e, weight=freq)

    return G, filtered_pairs


def create_analogy_network(analogy_pairs, min_frequency=1):
    """
    Create a directed network for 'aku ... dia' or 'dia ... aku' analogies.
    Each relation is represented as (subject, phrase) → (other_subject, phrase).
    """
    G = nx.DiGraph()

    # Convert analogy pairs into edges
    pair_counter = Counter()
    for (subj1, phrase1, subj2, phrase2) in analogy_pairs:
        pair_counter[((f"{subj1} {phrase1}", f"{subj2} {phrase2}"))] += 1

    filtered_pairs = [(pair, freq) for pair, freq in pair_counter.items() if freq >= min_frequency]

    for (node1, node2), freq in filtered_pairs:
        G.add_edge(node1, node2, weight=freq)

    return G, filtered_pairs

# Plotting Function

def plot_network(G, filtered_pairs, title, node_colors=None, figsize=(12, 8)):
    """
    Plot and save a network graph.
    """
    plt.figure(figsize=figsize)

    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

    # Edge weights
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    edge_widths = [w / max_weight * 5 for w in weights]

    # Node sizes
    node_sizes = []
    for node in G.nodes():
        base_size = G.degree(node) * 300 + 500
        node_sizes.append(base_size)

    # Default node colors
    if node_colors is None:
        # Separate emoji and word nodes
        emoji_nodes = [node for node in G.nodes() if any(ord(char) > 127 for char in str(node))]
        word_nodes = [node for node in G.nodes() if node not in emoji_nodes]
        
        node_colors = []
        for node in G.nodes():
            if node in emoji_nodes:
                node_colors.append('#FFD700')  # Gold for emoji
            else:
                node_colors.append('#87CEEB')  # Sky blue for words

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes, node_color=node_colors,
        alpha=0.8, edgecolors='black', linewidths=1
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos, width=edge_widths, alpha=0.6,
        edge_color='gray', arrows=True, arrowsize=20
    )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Draw edge labels
    edge_labels = {(u, v): f"{G[u][v]['weight']}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title(title, size=16, weight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"../data/{title.replace(' ', '_').lower()}.png", dpi=300)
    return plt

# Analogy Extraction Function

def extract_aku_dia(text):
    """
    Extract patterns like:
    - "aku ... dia ..."
    - "dia ... aku ..."
    Returns list of tuples: (subject1, phrase1, subject2, phrase2)
    """
    pairs = []

    # Pattern 1: "aku ... dia ..."
    matches1 = re.findall(r"aku\s+([^.,!?]+).*dia\s+([^.,!?]+)", text)
    for m in matches1:
        pairs.append(("aku", m[0].strip(), "dia", m[1].strip()))

    # Pattern 2: "dia ... aku ..."
    matches2 = re.findall(r"dia\s+([^.,!?]+).*aku\s+([^.,!?]+)", text)
    for m in matches2:
        pairs.append(("dia", m[0].strip(), "aku", m[1].strip()))

    # Save pairs to a text file
    with open("../data/aku_dia_analogies.txt", "a", encoding="utf-8") as f:
        for p in pairs:
            f.write(f"{p[0]}: {p[1]} | {p[2]}: {p[3]}\n")

    return pairs