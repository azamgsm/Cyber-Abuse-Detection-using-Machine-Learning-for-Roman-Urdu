# train_models.py - teeno models train karke models.pkl mein save karta hai
# Chalane ka tareeqa:  python train_models.py
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from text_utils import clean_text

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "Cyber_Abuse_Dataset.csv", keep_default_na=False, na_values=[""])
df = df.dropna().drop_duplicates(subset=["Comments"])
texts = df["Comments"].apply(clean_text)
y = (df["Classes"].str.strip().str.upper() == "A").astype(int)  # A=1, NA=0

X_train, X_test, y_train, y_test = train_test_split(
    texts, y, test_size=0.25, random_state=42, stratify=y)

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
train_features = vectorizer.fit_transform(X_train)
test_features = vectorizer.transform(X_test)

models = {
    "Linear SVM": SVC(kernel="linear"),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Multinomial Naive Bayes": MultinomialNB(),
}

metrics, matrices = {}, {}
for name, model in models.items():
    model.fit(train_features, y_train)
    pred = model.predict(test_features)
    metrics[name] = {
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred, zero_division=0),
        "Recall": recall_score(y_test, pred, zero_division=0),
        "F1-score": f1_score(y_test, pred, zero_division=0),
    }
    matrices[name] = confusion_matrix(y_test, pred, labels=[0, 1]).tolist()
    print(name, {k: round(v, 3) for k, v in metrics[name].items()}, matrices[name])

joblib.dump({"vectorizer": vectorizer, "models": models, "metrics": metrics,
             "matrices": matrices, "test_size": len(y_test)}, BASE / "models.pkl")
print("Saved: models.pkl")
