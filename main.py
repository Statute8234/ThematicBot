import re
import collections
import nltk
import string
import random
from nltk.corpus import wordnet
nltk.download('wordnet')
from fuzzywuzzy import fuzz

dictionary = {
    "Introduction": {
        "Input": ["Hello", "Hi"],
        "Response": ["Welcome","Hey"]
    },
    "Ceche": {
        "Input": ["bye","Goodbye"],
        "Response": ["see you","Thankyou"]
    }
}

""" part 2 passive way to detect the users emotions """



""" part 1 need to add new theme """

# make a theme name
# Preload words from WordNet by part of speech
word_lists_by_pos = {
    pos: list(set(lemma.name() for synset in wordnet.all_synsets(pos) for lemma in synset.lemmas()))
    for pos in ['n', 'v', 'a']  # Nouns, verbs, adjectives
}

def get_words_by_pos(pos):
    """ Fetch preloaded words from WordNet by part of speech (pos) """
    return word_lists_by_pos[pos]

def create_new_word(pos='n'):
    """ Create a new word by blending parts of existing words """
    words = get_words_by_pos(pos)
    return random.choice(words)

def analyze_themes(dictionary):
    attempts = 0
    while True:
        ThemeName = create_new_word(pos=random.choice(['n', 'v', 'a']))
        for existing_theme_name in dictionary:
            ratio = fuzz.ratio(existing_theme_name, ThemeName)
            if ratio >= 70 and existing_theme_name != ThemeName:
                return ThemeName

# transfer ceche
def transfer_ceche(dictionary):
    if "Ceche" in dictionary and dictionary["Ceche"]["Input"]:
        # Suggest new theme name based on Ceche pattern
        new_theme_name = analyze_themes(dictionary)
        if new_theme_name:
            # Create new theme using Ceche's input and response
            new_inputs = dictionary["Ceche"]["Input"]
            new_responses = dictionary["Ceche"]["Response"]
            add_theme(new_theme_name, new_inputs, new_responses)
            # Clear Ceche's entries after transferring
            dictionary["Ceche"]["Input"] = []
            dictionary["Ceche"]["Response"] = []
            return f"New theme '{new_theme_name}' added successfully."
        else:
            return "Failed to generate a unique new theme name."
    return "No patterns available in 'Ceche' to transfer."

# make a new theme
def add_theme(theme_name, input_list, response_list):
    """Add a new theme to the dictionary if it does not already exist."""
    if theme_name and theme_name not in dictionary:
        dictionary[theme_name] = {
            "Input": input_list,
            "Response": response_list
        }
        print(f"Theme '{theme_name}' added successfully.")
    else:
        print(f"Theme '{theme_name}' already exists or was not provided.")

# Example use of the functions
print("Current dictionary:", dictionary)
result = transfer_ceche(dictionary)
print(result)
print("Updated dictionary:", dictionary)