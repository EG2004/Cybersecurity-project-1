# ml_model.py

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Use correct columns
texts = df["Query"]
labels = df["Label"]

# Convert text → numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42
)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)


# Function for app
def ml_detection(user_input):
    input_vector = vectorizer.transform([user_input])
    prediction = model.predict(input_vector)[0]

    if prediction == 1:
        return "🚨 ML: SQL Injection Detected"
    else:
        return "✅ ML: Input Looks Safe"
