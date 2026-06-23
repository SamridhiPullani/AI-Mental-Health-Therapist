import random

positive_responses = [
    "That's wonderful! Keep believing in yourself 🌟",
    "You seem to be in a good mood today 😊",
    "Great to hear that! Keep smiling 💖"
]

negative_responses = [
    "I'm sorry you're feeling this way 💛",
    "Take a deep breath. Tomorrow can be better 🌿",
    "Remember, difficult moments don't last forever 🤗"
]

neutral_responses = [
    "I understand. Tell me more about it.",
    "How has your day been so far?",
    "I'm listening. Feel free to share."
]

def get_therapy_response(mood):
    if "Positive" in mood:
        return random.choice(positive_responses)
    elif "Negative" in mood:
        return random.choice(negative_responses)
    else:
        return random.choice(neutral_responses)