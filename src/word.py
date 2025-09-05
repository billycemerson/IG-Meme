import pandas as pd
from prep import clean_comment
from graph_word import (
    create_word_network, create_word_emoji_network,
    create_analogy_network, plot_network, extract_aku_dia
)
from collections import Counter
import re
import emoji
import itertools
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Load and preprocess data
data = pd.read_csv('../data/comments.csv')
data = data.drop(columns=['parent_id'])
data['comment_time'] = pd.to_datetime(data['comment_time'], unit='s')
data['date'] = data['comment_time'].dt.date

# Clean text
data['clean_comment'] = data['comment'].apply(clean_comment)
data = data.dropna(subset=['clean_comment']).reset_index(drop=True)

# Utility function
def extract_emojis(text):
    return [ch for ch in text if ch in emoji.EMOJI_DATA]

# Word-to-Word Pairs
word_pairs = []
for comment in data['clean_comment']:
    words = re.findall(r'\w+', comment)
    if len(words) > 1:
        word_pairs.extend(itertools.combinations(sorted(set(words)), 2))

word_pair_freq = Counter(word_pairs).most_common(20)

# Word-to-Emoji Pairs
word_emoji_pairs = []
for comment in data['clean_comment']:
    ems = extract_emojis(comment)
    words = re.findall(r'\w+', comment)
    for w in words:
        for e in ems:
            word_emoji_pairs.append((w, e))

word_emoji_freq = Counter(word_emoji_pairs).most_common(20)

# Aku vs Dia Analogy
analogy_pairs = []
for comment in data['clean_comment']:
    analogy_pairs.extend(extract_aku_dia(comment))

# Word-to-Word
G_word, filtered_word_pairs = create_word_network(word_pair_freq, min_frequency=2)
plot_network(G_word, filtered_word_pairs, "Word-to-Word")

# Word-to-Emoji
G_we, filtered_we_pairs = create_word_emoji_network(word_emoji_freq, min_frequency=2)
plot_network(G_we, filtered_we_pairs, "Word-to-Emoji")

# Aku vs Dia Analogy
G_analogy, filtered_analogy = create_analogy_network(analogy_pairs, min_frequency=1)
plot_network(G_analogy, filtered_analogy, "Aku-vs-Dia", figsize=(15, 10))