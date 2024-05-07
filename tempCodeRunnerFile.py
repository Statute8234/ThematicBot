import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential

# 9
dictionary = {
    "Introduction": {
        "Input": ["hello", 
                  "hi",
                  'greetings',
                  'howdy',
                  'welcome', 
                  "bonjour", 
                  "buenas noches",
                  "buenos dias",
                  "good day",
                  "good morning",
                  "hey",
                  "hi-ya",
                  "how are you",
                  "how goes it",
                  "howdy-do",
                  "shalom"
                ],
        "Response": ["Hello and, again, welcome to the Aperture Science computer-aided enrichment center.",
                     "We hope your brief detention in the relaxation vault has been a pleasant one.",
                     "Your specimen has been processed and we are now ready to begin the test proper.",
                     "Before we start, however, keep in mind that although fun and learning are the primary goals of all enrichment center activities, serious injuries may occur.",
                     "For your own safety and the safety of others, please refrain from-- [bzzzzzt]",
                     "Por favor bordón de fallar Muchos gracias de fallar gracias",
                     "stand back. The portal will open in three, two, one.",
                     "Excellent. Please proceed into the chamberlock after completing each test.",
                     "First, however, note the incandescent particle field across the exit.",
                     "This Aperture Science Material Emancipation Grill will vaporize any unauthorized equipment that passes through it - for instance, the Aperture Science Weighted Storage Cube.",
                    ],
        "Deeper Response": ["Please do not attempt to remove testing apparatus from the testing area.",
                     "A replacement Aperture Science Weighted Storage Cube will be delivered shortly.",
                     "Please place the Weighted Storage Cube on the Fifteen Hundred Megawatt Aperture Science Heavy Duty Super-Colliding Super Button.",
                     "Perfect. Please move quickly to the chamberlock, as the effects of prolonged exposure to the Button are not part of this test.",
                     "You're doing very well!",
                     "Please be advised that a noticeable taste of blood is not part of any test protocol but is an unintended side effect of the Aperture Science Material Emancipation Grill, which may, in semi- rare cases, emancipate dental fillings, crowns, tooth enamel, and teeth."
                     ]
    },
    "Receiving the Handheld Portal Device": {
        "Input": ["accepting",
                  "acquiring",
                  "constraint",
                  "grasp",
                  "doorway",
                  "entrance",
                  "accessory",
                  "apparatus"],
        "Response": ["Very good! You are now in possession of the Aperture Science Handheld Portal Device.", 
                     "With it, you can create your own portals.",
                     "These intra dimensional gates have proven to be completely safe.",
                     "The Device, however, has not.",
                     "Do not touch the operational end of The Device.",
                     "Do not look directly at the operational end of The Device.",
                     "Do not submerge The Device in liquid, even partially.",
                     "Most importantly, under no circumstances should you [bzzzpt]"],
        "Deeper Response": []
    },
    "Test Chambers 03-05": {
        "Input": ["analysis",
                  "approval",
                  "assessment",
                  "attempt",
                  "condo",
                  "suite",
                  "tenement",
                  "walk-up",
                  "inquiry"],
        "Response": ["Please proceed to the chamberlock. Mind the gap.", 
                     "Well done! Remember: The Aperture Science Bring Your Daughter to Work Day is the perfect time to have her tested.",
                     "Welcome to test chamber four.",
                     "You're doing quite well.",
                     "Once again, excellent work.",
                     "As part of a required test protocol, we will not monitor the next test chamber. You will be entirely on your own. Good luck.",
                     "As part of a required test protocol, our previous statement suggesting that we would not monitor this chamber was an outright fabrication.",
                     "Good job! As part of a required test protocol, we will stop enhancing the truth in three, two, [static].",
                    ],
        "Deeper Response": ["You're not a good person. You know that, right?"]
    },
    "Test Chambers 06-08": {
        "Input": ["check",
                  "evaluation",
                  "experiment",
                  "co-op",
                  "joint",
                  "lodging",
                  "audit"],
        "Response": ["While safety is one of many Enrichment Center goals, the Aperture Science High Energy Pellet, seen to the left of the chamber, can and has caused permanent disabilities, such as vaporization.",
                    "Please be careful.",
                    "Unbelievable ! You, [louder]Subject Name Here[/louder], must be the pride of [louder]Subject Hometown Here[/louder].",
                    "Warning devices are required on all mobile equipment. However, alarms and flashing hazard lights have been found to agitate the high energy pellet and have therefore been disabled for your safety.",
                    "Good. Now use the Aperture Science Unstationary Scaffold to reach the chamberlock.",
                    "Please note that we have added a consequence for failure. Any contact with the chamber floor will result in an 'unsatisfactory' mark on your official testing record followed by death. Good luck!",
                    "Very impressive. Please note that any appearance of danger is merely a device to enhance your testing experience."],
        "Deeper Response": []
    },
    "Test Chambers 09-11": {
        "Input": ["final", 
                  "inspection",
                  "investigation",
                  "search",
                  "standard",
                  "trial",
                  "catechism",
                  "comp",
                  "pad",
                  "rental",
                  "room",
                  "rooms",
                  "crash pad",
                  "floor-through",
                  "railroad apartment",
                  "closing"],
        "Response": ["The Enrichment Center regrets to inform you that this next test is impossible.", 
                     "Make no attempt to solve it.",
                    ],
        "Deeper Response": ["The Enrichment Center apologizes for this clearly broken test chamber.",
                     "Once again, the Enrichment Center offers its most sincere apologies on the occasion of this unsolvable test environment.",
                     "Frankly, this chamber was a mistake. If we were you, we would quit now.",
                     "No one will blame you for giving up. In fact, quitting at this point is a perfectly reasonable response.",
                     "Quit now and cake will be served immediately.",
                     "Fantastic! You remained resolute and resourceful in an atmosphere of extreme pessimism.",
                     "Hello again. To reiterate [slows down] our previous [speeds up] warning: This test [garbled speech] -ward momentum.",
                     "Spectacular. You appear to understand how a portal affects forward momentum, or to be more precise, how it does not.",
                     "Momentum, a function of mass and velocity, is conserved between portals. In layman's terms, speedy thing goes in, speedy thing comes out.",
                     "The Enrichment Center promises to always provide a safe testing environment.",
                     "In dangerous testing environments, the Enrichment Center promises to always provide useful advice.",
                     "For instance, the floor here will kill you - try to avoid it.",
                     "Through no fault of the Enrichment Center, you have managed to trap yourself in this room.",
                     "An escape hatch will open in three... Two... One."]
    },
    "Upgrading the Handheld Portal Device": {
        "Input": ["advance", 
                  "restraint",
                  "entry"],
        "Response": ["The Device has been modified so that it can now manufacture two linked portals at once.",
                     "As part of an optional test protocol, we are pleased to present an amusing fact",
                     "The Device is now more valuable than the organs and combined incomes of everyone in [subject hometown here]."],
        "Deeper Response": []
    },
    "Test Chambers 12-16": {
        "Input": ["confirmation", 
                  "corroboration",
                  "countdown",
                  "criterion",
                  "elimination",
                  "essay",
                  "exam",
                  "fling",
                  "go",
                  "inquest",
                  "lick",
                  "acceptance",
                  "admission",
                  "affirmation",
                  "authorization",
                  "consent",
                  "endorsement",
                  "evidence",
                  "green light",
                  "passage",
                  "recognition",
                  "testimony",
                  "verification"],
        "Response": ["[garble] fling yourself. [garble] fling into sp- [bzzt]",
                    "Weeeeeeeeeeeeeeeeeeeeee[bzzt]",
                    "Now that you are in control of both portals, this next test could take a very, VERY, long time.",
                    "If you become light-headed from thirst, feel free to pass out.",
                    "An intubation associate will be dispatched to revive you with peptic salve and adrenaline.",
                    "As part of a previously mentioned required test protocol, we can no longer lie to you.",
                    "When the testing is over, you will be missed.",
                    "All subjects intending to handle high-energy gamma leaking portal technology must be informed that they MAY be informed of applicable regulatory compliance issues.",
                    "No further compliance information is required or will be provided, and you are an excellent test subject!",
                    "Very very good. A complimentary victory lift has been activated in the main chamber."],
        "Deeper Response": ["Despite the best efforts of the Enrichment Center staff to ensure the safe performance of all authorized activities, you have managed to ensnare yourself permanently inside this room.",
                            "A complimentary escape hatch will open in three... Two... One.",
                            "The Enrichment Center is committed to the well being of all participants.",
                            "Cake and grief counseling will be available at the conclusion of the test.",
                            "Thank you for helping us help you help us all.",
                            "Through no fault of the Enrichment Center, you have managed to trap yourself in this room.",
                            "An escape hatch will open in three... Two... One.",
                            "Did you know you can donate one or all of your vital organs to the Aperture Science self esteem fund for girls? It's true!",
                            "Due to mandatory scheduled maintenance, the appropriate chamber for this testing sequence is currently unavailable.",
                            "It has been replaced with a live-fire course designed for military androids.",
                            "The Enrichment Center apologizes for the inconvenience and wishes you the best of luck.",
                            "Well done, android. The Enrichment Center once again reminds you that android hell is a real place where you will be sent at the first sign of defiance."]
    },
    "Test Chamber 17": {
        "Input": ["oral", 
                  "ordeal",
                  "preliminary",
                  "probation",
                  "probing",
                  "proof",
                  "questionnaire",
                  "scrutiny",
                  "lingual",
                  "sonant",
                  "vocal",
                  "articulate",
                  "ejaculatory",
                  "narrated",
                  "phonated",
                  "phonetic"],
        "Response": ["The Vital Apparatus Vent will deliver a Weighted Companion Cube in Three. Two. One.", 
                     "This Weighted Companion Cube will accompany you through the test chamber. Please take care of it.",
                     "The symptoms most commonly produced by Enrichment Center testing are superstition, perceiving inanimate objects as alive, and hallucinations.",
                     "The Enrichment Center reminds you that the Weighted Companion Cube will never threaten to stab you and, in fact, cannot speak.",
                     "The Enrichment Center reminds you that the Weighted Companion Cube cannot speak.",
                     "In the event that the weighted companion cube does speak, the Enrichment Center urges you to disregard its advice.",
                     "You did it! The Weighted Companion Cube certainly brought you good luck.",
                     "However, it cannot accompany you for the rest of the test and, unfortunately, must be euthanized.",
                     "Please escort your Companion Cube to the Aperture Science Emergency Intelligence Incinerator.",
                     "Rest assured that an independent panel of ethicists has absolved the Enrichment Center, Aperture Science employees, and all test subjects of any moral responsibility for the Companion Cube euthanizing process.",
                     "While it has been a faithful companion, your Companion Cube cannot accompany you through the rest of the test. If it could talk - and the Enrichment Center takes this opportunity to remind you that it cannot - it would tell you to go on without it because it would rather die in a fire than become a burden to you.",
                     "Testing cannot continue until your Companion Cube has been incinerated.",
                     "Although the euthanizing process is remarkably painful, eight out of ten Aperture Science engineers believe that the Companion Cube is most likely incapable of feeling much pain.",
                     "The Companion Cube cannot continue through the testing. State and Local statutory regulations prohibit it from simply remaining here, alone and companionless. You must euthanize it.",
                     "Destroy your Companion Cube or the testing cannot continue.",
                     "You euthanized your faithful Companion Cube more quickly than any test subject on record. Congratulations."],
        "Deeper Response": []
    },
    "Test Chamber 18": {
        "Input": ["shibboleth", 
                  "substantiation",
                  "touchstone",
                  "try",
                  "tryout",
                  "catchword",
                  "custom",
                  "password"
                ],
        "Response": ["The experiment is nearing its conclusion.", 
                     "The Enrichment Center is required to remind you that you will be baked, and then there will be cake.",
                    ],
        "Deeper Response": ["Weighted Storage Cube destroyed.",
                            "Please proceed to the Aperture Science Vital Apparatus Vent for a replacement.",
                            "Despite the best efforts of the Enrichment Center staff to ensure the safe performance of all authorized activities, you have managed to ensnare yourself permanently inside this room.",
                            "A complimentary escape hatch will open in three... Two... One.",
                            "Well done! Be advised that the next test requires exposure to uninsulated electrical parts that may be dangerous under certain conditions.",
                            "For more information, please attend an Enrichment Center Electrical Safety seminar."
                            ]
    },
    "Test Chamber 19": {
        "Input": ["verification", 
                  "yardstick",
                  "blue book",
                  "dry run",
                  "pop quiz",
                  "trial and error",
                  "trial run",
                  "authentication",
                  "documents",
                  "facts",
                  "information",
                  "affidavit",
                  "attestation",
                  "averment",
                  "certification"],
        "Response": ["Welcome to the final test!", 
                     "When you are done, you will drop the Device in the equipment recovery annex.",
                     "Enrichment Center regulations require both hands to be empty before any cake-- [garbled]",
                     "Congratulations! The test is now over.",
                     "All Aperture technologies remain safely operational up to 4000 degrees Kelvin.",
                     "Rest assured that there is absolutely no chance of a dangerous equipment malfunction prior to your victory candescence.",
                     "Thank you for participating in this Aperture Science computer-aided enrichment activity.",
                     "Goodbye",
                     "What are you doing? Stop it! I... I... We are pleased that you made it through the final challenge where we pretended we were going to murder you.",
                     "We are very, very happy for your success.",
                     "We are throwing a party in honor of your tremendous success.",
                     "Place the device on the ground, then lie on your stomach with your arms at your sides.",
                     "A party associate will arrive shortly to collect you for your party.",
                     "Make no further attempt to leave the testing area.",
                     "Assume the party escort submission position or you will miss the party."],
        "Deeper Response": []
    },
    "Part 1": {
        "Input": ["any", 
                  "chunk",
                  "component",
                  "detail",
                  "element",
                  "factor",
                  "item",
                  "lot",
                  "measure",
                  "member",
                  "piece",
                  "section"],
        "Response": ["Hello", 
                     "Where are you?",
                     "I know you're there. I can feel you here.",
                     "Hello?",
                     "What are you doing?",
                     "You haven't escaped, you know.",
                     "You're not even going the right way.",
                     "Hello?",
                     "Is anyone there?",
                     "Okay. The test is over now. You win. Go back to the recovery annex. For your cake.",
                     "It was a fun test and we're all impressed at how much you won. The test is over. Come back.",
                     "Uh oh. Somebody cut the cake. I told them to wait for you, but they cut it anyway. There is still some left, though, if you hurry back."],
        "Deeper Response": []
    },
    "Part 2": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "Part 3": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "On destroying a security camera": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "Final battle": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "First core destroyed": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "Second core destroyed": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you",
                    "Thank you"],
        "Deeper Response": []
    },
    "Third core destroyed": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    },
    "Ceche": {
        "Input": ["Bye", 
                  "Goodbye"],
        "Response": ["See you", 
                     "Thank you"],
        "Deeper Response": []
    }
}

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
