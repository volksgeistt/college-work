"""
for the given dataset, 'Heart.csv', divide the dataset into training and testing sets.
Implement a decision tree classifier and evaluate the model using evaluation metrics.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

df = pd.read_csv("heart.csv")

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Original Dataset Shape:", X.shape)
print("Training Feature Shape:", X_train.shape)
print("Testing Feature Shape:", X_test.shape)

print("Original Target Shape:", y.shape)
print("Training Target Shape:", y_train.shape)
print("Testing Target Shape:", y_test.shape)

model = DecisionTreeClassifier(random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)


print("\nEvaluation Metrics")
print("Accuracy :", accuracy)
print("Recall   :", recall)
print("Precision:", precision)
print("F1 Score :", f1)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
