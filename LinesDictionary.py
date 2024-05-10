"""
1) change the dictionary keys
2) change Input list words to make better words to fit the Response or Deeper Responses
3) Then Make one mkore skript that would make a new responce the fits the users input perfectly.
4) Maybe add the reult from number 3, to the chehe
"""

import spacy
import numpy as np
from sklearn.cluster import KMeans
import neural_network_classifier, LinesDictionary
nlp = spacy.load('en_core_web_md')

dictionary = LinesDictionary.dictionary

# Function to average word vectors
def get_average_vector(texts):
    vectors = [nlp(text).vector for text in texts if nlp(text).vector_norm > 0]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros((nlp.vocab.vectors_length,))

# Aggregate texts and compute their average vectors
text_vectors = {}
for key, values in dictionary.items():
    aggregated_texts = values['Input'] + values['Response'] + values['Deeper Response']
    text_vectors[key] = get_average_vector(aggregated_texts)

# Print new keys
def change_keys():
    keys = list(text_vectors.keys())
    vectors = np.array(list(text_vectors.values()))
    kmeans = KMeans(n_clusters=2, random_state=42).fit(vectors)
    new_keys = ["Category_" + str(label) for label in kmeans.labels_]
    # --
    for key, new_key in zip(keys, new_keys):
        dictionary[new_key] = dictionary[key]
        del dictionary[key]
