import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib as jl     # fast calculation

df=pd.read_csv("heart.csv")  #read the data
df=pd.DataFrame(df)

# parameter   importance in ratings(⭐)
# ======================================
# age             1
# sex             1
# cp              4
# trestbps        2
# chol            2
# fbs             1
# restecg         2
# thalach         4
# exang           4
# oldpeak         4
# slope           3
# ca              4
# thal            4
# ======================================
# target          1 means heart disease exists.
#                 0 means heart disease doesn't exist.
# ======================================

averages=df.groupby('sex')['chol'].mean()       # Basic visualization

plt.bar(averages.index, averages.values, tick_label=['0', '1'])     # Plot
plt.xlabel('X values')
plt.ylabel('Average Y (90 < Y < 300)')
plt.title('Average Y for X = 0 and X = 1')
# plt.show()

X = df.drop('target', axis=1)       # Features (all columns except 'target')

y = df['target']        # Target

# print(X.head())     # Quick check
# print(y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# print("Training set shape:", X_train.shape)
# print("Testing set shape:", X_test.shape)

scaler=StandardScaler()     # create a scaler object

X_train_scaled = scaler.fit_transform(X_train)      # Fit the scaler on training data and transform both training and testing data
X_test_scaled = scaler.transform(X_test)

# print(X_train_scaled[:5])  # first 5 rows of scaled training data

model = RandomForestClassifier(n_estimators=100, random_state=42)  # create a model
model.fit(X_train_scaled, y_train)      # model training

y_pred = model.predict(X_test_scaled)   # predict the test data

# print("Accuracy:", accuracy_score(y_test, y_pred))  # evaluation
# print(classification_report(y_test, y_pred))

jl.dump(model, "heart_model.pkl")       # Save the training model
jl.dump(scaler, "scaler.pkl")           # Save the scaler

# Load model
model = jl.load("heart_model.pkl")

# Load scaler
scaler = jl.load("scaler.pkl")

# Predict new data
# new_data_scaled = scaler.transform(new_data)
# prediction = model.predict(new_data_scaled)