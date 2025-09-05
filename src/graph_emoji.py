from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx

# Graph emoji to emoji network
def create_emoji_network(emoji_pairs, min_frequency=1):

    G = nx.DiGraph()
    
    # Filter based on minimum freq
    filtered_pairs = [(pair, freq) for pair, freq in emoji_pairs if freq >= min_frequency]
    
    # Add edges and weight
    for (emoji1, emoji2), freq in filtered_pairs:
        G.add_edge(emoji1, emoji2, weight=freq)
    
    return G, filtered_pairs

# Graph emoji to word network
def create_emoji_word_network(emoji_word_pairs, min_frequency=1):

    G = nx.DiGraph()
    
    # Filter based on minimum freq
    filtered_pairs = [(pair, freq) for pair, freq in emoji_word_pairs if freq >= min_frequency]
    
    # Add edges and weight
    for (emoji, word), freq in filtered_pairs:
        G.add_edge(emoji, word, weight=freq)
    
    return G, filtered_pairs

# Function for plot network
def plot_network(G, filtered_pairs, title, node_colors=None, figsize=(12, 8)):

    plt.figure(figsize=figsize)
    
    # Layout for positioning nodes
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Prepare edge weights
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    
    # Normalize edge weights
    edge_widths = [w / max_weight * 5 for w in weights]
    
    # Node sizes based on degree and type (emoji or word)
    node_sizes = []
    emoji_size_multiplier = 2.0
    
    for node in G.nodes():
        base_size = G.degree(node) * 300 + 500
        # Check if caharacter contain ASCII
        if any(ord(char) > 127 for char in str(node)):
            node_sizes.append(base_size * emoji_size_multiplier) 
        else:
            node_sizes.append(base_size)  # Word normal size
    
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
    
    # Draw network
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, 
                          alpha=0.8, edgecolors='black', linewidths=1)
    
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, 
                          edge_color='gray', arrows=True, arrowsize=20)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Add edge labels (weights)
    edge_labels = {(u, v): f"{G[u][v]['weight']}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    
    plt.title(title, size=16, weight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"../data/{title.replace(' ', '_').lower()}.png", dpi=300)
    return plt