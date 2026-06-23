from textblob import TextBlob

def analyze_mood(text):
    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😔"
    else:
        return "Neutral 😐"