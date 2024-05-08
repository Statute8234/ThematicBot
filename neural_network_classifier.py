import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
import ThematicBot, LinesDictionary

dictionary = LinesDictionary.dictionary
ThematicBot.change_keys()
# Preparing data for training
inputs = []
labels = []
responses = {}
deeper_responses = {}

for key, value in dictionary.items():
    inputs.extend(value['Input'])
    labels.extend([key] * len(value['Input']))
    responses[key] = value['Response']
    deeper_responses[key] = value['Deeper Response']

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Tokenize inputs
tokenizer = Tokenizer()
tokenizer.fit_on_texts(inputs)
max_len = max(len(x.split()) for x in inputs)
vocab_size = len(tokenizer.word_index) + 1

# Convert text inputs to sequences
sequences = tokenizer.texts_to_sequences(inputs)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Split data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, encoded_labels, test_size=0.2, random_state=42)

# Building a simple neural network
model = Sequential([
    Embedding(vocab_size, 10, input_length=max_len),
    GlobalAveragePooling1D(),
    Dense(len(set(labels)), activation='softmax')
])
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))

# Function to predict and return response
def predict_response(text, deep=False):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_len)
    pred = model.predict(padded)
    label = label_encoder.inverse_transform([np.argmax(pred)])
    if deep and deeper_responses[label[0]]:
        selected_response = np.random.choice(deeper_responses[label[0]])
    else:
        selected_response = np.random.choice(responses[label[0]])
    return selected_response