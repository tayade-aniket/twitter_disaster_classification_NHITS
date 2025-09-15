import streamlit as st
import pickle
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# -------------------------------------------------
# Load the trained model and vectorizer
# -------------------------------------------------
with open("disaster_tweet_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# -------------------------------------------------
# Text preprocessing function
# -------------------------------------------------
def preprocess_text(text: str) -> str:
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)       # remove URLs
    text = re.sub(r"@\w+", "", text)                         # remove @mentions
    text = re.sub(r"#", "", text)                            # remove hashtags symbol only
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)                          # remove digits
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.title("🚨 Disaster Tweet Classifier")
st.write("Enter a tweet to check if it’s about a **Disaster** or **Non-Disaster**.")

tweet_text = st.text_area("Tweet Text", placeholder="Type or paste a tweet here...")

if st.button("Predict"):
    if tweet_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Preprocess and predict
        processed_text = preprocess_text(tweet_text)
        features = vectorizer.transform([processed_text])
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        result = "Disaster" if prediction == 1 else "Non-Disaster"
        confidence = probability if prediction == 1 else (1 - probability)

        st.subheader("Prediction")
        st.write(f"**Result:** {result}")
        st.write(f"**Confidence:** {confidence * 100:.2f}%")
