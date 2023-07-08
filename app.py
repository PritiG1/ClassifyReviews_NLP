import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

# Create Flask app
app = Flask(__name__)

# Load the pickle model
model = joblib.load(open('logistic_regression_NLPreviews.joblib', 'rb'))

# Load the vectorizer
vectorizer = joblib.load('vectorizer_reviews.joblib')

@app.route("/")
def Home():
    return render_template("index1.html")

# Define a route for the prediction endpoint
@app.route('/predict', methods=["POST"])

def predict():
    review = request.form['Review']  # Get the review from the form

    #Preprocess the review
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    all_stopwords.remove('no')
    all_stopwords.remove('but')
    all_stopwords.remove("won't")
    all_stopwords.remove("too")
    all_stopwords.remove("very")
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    print(review)

    
    # Vectorize the review using the loaded vectorizer
    review_vectorized = vectorizer.transform([review])

    # Make predictions using the loaded model
    prediction = model.predict(review_vectorized)

    # Convert the prediction to sentiment labels
    sentiment = "positive" if prediction[0] == 1 else "negative"

    return render_template("index1.html", prediction_text="The sentiment is {}".format(sentiment))

# Run the app if executed directly
if __name__ == "__main__":
    app.run(debug=True)