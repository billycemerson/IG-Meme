import pandas as pd
from prep import clean_comment
from graph_emoji import (
    create_emoji_network, create_emoji_word_network, plot_network
)
from collections import Counter
import re
import emoji
import itertools
import matplotlib.pyplot as plt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# read data
data = pd.read_csv('../data/comments.csv')
# ignore columns parent_id
data = data.drop(columns=['parent_id'])

# convert comment_time to datetime
data['comment_time'] = pd.to_datetime(data['comment_time'], unit='s')
# extract date from comment_time
data['date'] = data['comment_time'].dt.date

# Cleaning comment_text
data['clean_comment'] = data['comment'].apply(clean_comment)
# drop null or empty
data = data.dropna(subset=['clean_comment']).reset_index(drop=True)

# Function to extract emojis from text
def extract_emojis(text):
    return [ch for ch in text if ch in emoji.EMOJI_DATA]

# 1. Emoji Frequency
all_emojis = []
for comment in data['clean_comment']:
    all_emojis.extend(extract_emojis(comment))

# 2. Emoji Co-occurrence (pairs in same comment)
emoji_pairs = []
for comment in data['clean_comment']:
    ems = extract_emojis(comment)
    if len(ems) > 1:
        emoji_pairs.extend(itertools.combinations(sorted(set(ems)), 2))

# 3. Emoji–Word Association
emoji_word_pairs = []
for comment in data['clean_comment']:
    ems = extract_emojis(comment)
    words = re.findall(r'\w+', comment)
    for e in ems:
        for w in words:
            emoji_word_pairs.append((e, w))

emoji_pair_freq = Counter(emoji_pairs).most_common(20)
emoji_word_freq = Counter(emoji_word_pairs).most_common(20)

# Plot Emoji-to-Emoji Network
G_emoji, filtered_emoji_pairs = create_emoji_network(emoji_pair_freq, min_frequency=1)
plot_network(G_emoji, filtered_emoji_pairs, 
            "Emoji-to-Emoji",
            node_colors=['#FFD700'] * len(G_emoji.nodes()))

# Plot Emoji-to-Word Network  
G_word, filtered_word_pairs = create_emoji_word_network(emoji_word_freq, min_frequency=2)
plot_network(G_word, filtered_word_pairs, 
            "Emoji-to-Word",
            figsize=(15, 10))