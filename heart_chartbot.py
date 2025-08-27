import pandas as pd
import joblib

# Load saved model and scaler
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

# Function to get valid integer input
def get_int(prompt, valid_range=None):
    while True:
        try:
            value = int(input(prompt))
            if valid_range and value not in valid_range:
                print(f"❌ Invalid input! Enter one of {valid_range}")
            else:
                return value
        except ValueError:
            print("❌ Invalid input! Please enter an integer.")

# Function to get valid float input
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

print("💓 Welcome to the Heart Disease Prediction Chatbot!\nPlease answer the following questions:")

# Collecting user input
age = get_int("Age: ")
sex = get_int("Sex (0 = female, 1 = male): ", valid_range=[0,1])
cp = get_int("Chest pain type (0-3): ", valid_range=[0,1,2,3])
trestbps = get_int("Resting blood pressure: ")
chol = get_int("Cholesterol: ")
fbs = get_int("Fasting blood sugar > 120 mg/dl? (0 = no, 1 = yes): ", valid_range=[0,1])
restecg = get_int("Resting ECG (0-2): ", valid_range=[0,1,2])
thalach = get_int("Maximum heart rate achieved: ")
exang = get_int("Exercise induced angina? (0 = no, 1 = yes): ", valid_range=[0,1])
oldpeak = get_float("ST depression induced by exercise: ")
slope = get_int("Slope of ST segment (0-2): ", valid_range=[0,1,2])
ca = get_int("Number of major vessels colored by fluoroscopy (0-3): ", valid_range=[0,1,2,3])
thal = get_int("Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect): ", valid_range=[1,2,3])

# Convert input to DataFrame
user_data = pd.DataFrame({
    'age': [age],
    'sex': [sex],
    'cp': [cp],
    'trestbps': [trestbps],
    'chol': [chol],
    'fbs': [fbs],
    'restecg': [restecg],
    'thalach': [thalach],
    'exang': [exang],
    'oldpeak': [oldpeak],
    'slope': [slope],
    'ca': [ca],
    'thal': [thal]
})

# Scale input
user_data_scaled = scaler.transform(user_data)

# Predict
prediction = model.predict(user_data_scaled)

# Friendly output
print("\n🔎 Prediction Result:")
if prediction[0] == 1:
    print("⚠️ According to the model, there is a risk of heart disease. Please consult a doctor.")
else:
    print("✅ According to the model, no significant risk of heart disease was detected.")

print("\n💡 Note: This is an AI prediction tool, not a medical diagnosis.")
