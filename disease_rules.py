from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Load dataset
df = pd.read_csv("data/Diseases_symptoms.csv")

# Preprocess (fill NaN, encode symptoms as binary 1/0, etc.)
# Example assumes you already converted symptoms to columns
X = df.drop("disease", axis=1)
y = df["disease"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Prediction (assuming user input as binary vector)
def predict_disease(input_vector):
    result = model.predict([input_vector])[0]
    return result
