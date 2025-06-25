import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Download the UCI Heart Disease dataset (Cleveland)
url = "https://raw.githubusercontent.com/plotly/datasets/master/heart.csv"
df = pd.read_csv(url)

# Use only the available features that match your form:
X = df[['age', 'chol', 'trestbps']]
y = df['target']  # 1 = heart disease, 0 = no heart disease

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Save model
joblib.dump(clf, 'model_cdss.pkl')

print("Model trained and saved as model_cdss.pkl")
print("Features used:", list(X.columns))
