import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score

# Load saved model, scaler, and dataset
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")
df = pd.read_csv("heart.csv")

# Features and target
X = df.drop('target', axis=1)
y = df['target']

# Scale features
X_scaled = scaler.transform(X)

# Make predictions
y_pred = model.predict(X_scaled)

# -------------------------
# 1️⃣ Accuracy & Classification Report
# -------------------------
print("Accuracy:", accuracy_score(y, y_pred))
print("\nClassification Report:\n", classification_report(y, y_pred))

# -------------------------
# 2️⃣ Confusion Matrix
# -------------------------
cm = confusion_matrix(y, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Disease', 'Disease'])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# -------------------------
# 3️⃣ Feature Importance
# -------------------------
importances = model.feature_importances_
features = X.columns

# Create a DataFrame for plotting
feat_df = pd.DataFrame({'Feature': features, 'Importance': importances})
feat_df = feat_df.sort_values(by='Importance', ascending=False)

# Plot
plt.figure(figsize=(10,6))
sns.barplot(x='Importance', y='Feature', data=feat_df, palette='viridis')
plt.title("Feature Importance - Random Forest")
plt.show()

# -------------------------
# 4️⃣ Histogram of Predictions
# -------------------------
plt.figure(figsize=(6,4))
sns.countplot(y_pred)
plt.xticks([0,1], ['No Disease', 'Disease'])
plt.title("Predicted Class Distribution")
plt.show()
