import re

dictionary = {
    "Introduction": {
        "Input": ["Hello", "Hi"],
        "Responce": ["Welcome","Hey"]
    },
    "Ceche": {
        "Input": [],
        "Responce": []
    }
}

def normalize(string):
    string = re.sub(r'\W+', '', string.lower().split())
    return ''.join(string)

def find_best_Responce(input):
    bestScore = -1
    bestResponce = ""
    for theme, data in dictionary.items():
        score = 0
        # calculate
        for word in data['Input']:
            if word.lower() in input.lower().split():
                score += 1
        # if current score is highest
        if score > bestScore and data['Responce']:
            bestScore = score
            for item in data['Responce']:
                bestResponce += " " + normalize(item)
    return bestResponce

print(find_best_Responce("Hello"))
