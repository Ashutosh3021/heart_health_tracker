# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configure matplotlib for web usage
plt.switch_backend('Agg')
sns.set_style("whitegrid")

class HeartPredictor:
    """
    Heart Disease Prediction Class
    Handles model loading and predictions
    """
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load("heart_model.pkl")
            self.scaler = joblib.load("scaler.pkl")
            print("✅ Model and scaler loaded successfully!")
        except FileNotFoundError:
            print("❌ Model files not found. Please run heart_detector.py first!")
            self.model = None
            self.scaler = None
    
    def predict(self, user_data):
        """
        Make prediction based on user input
        Args:
            user_data (dict): Dictionary containing user health data
        Returns:
            dict: Prediction result and confidence
        """
        if self.model is None or self.scaler is None:
            return {"error": "Model not loaded"}
        
        # Convert input to DataFrame
        df = pd.DataFrame([user_data])
        
        # Scale the input data
        scaled_data = self.scaler.transform(df)
        
        # Make prediction
        prediction = self.model.predict(scaled_data)[0]
        confidence = self.model.predict_proba(scaled_data)[0]
        
        return {
            "prediction": int(prediction),
            "confidence": float(max(confidence)),
            "risk_percentage": float(confidence[1] * 100) if len(confidence) > 1 else 0
        }

# Initialize predictor
predictor = HeartPredictor()

@app.route('/')
def home():
    """Main page with prediction form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction request
    Receives form data and returns prediction result
    """
    try:
        # Get form data
        user_data = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trestbps': int(request.form['trestbps']),
            'chol': int(request.form['chol']),
            'fbs': int(request.form['fbs']),
            'restecg': int(request.form['restecg']),
            'thalach': int(request.form['thalach']),
            'exang': int(request.form['exang']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': int(request.form['slope']),
            'ca': int(request.form['ca']),
            'thal': int(request.form['thal'])
        }
        
        # Make prediction
        result = predictor.predict(user_data)
        
        if "error" in result:
            return jsonify({"error": result["error"]})
        
        # Format response
        response = {
            "success": True,
            "prediction": result["prediction"],
            "risk_percentage": round(result["risk_percentage"], 2),
            "confidence": round(result["confidence"], 2),
            "message": "⚠️ Higher risk detected. Please consult a doctor." if result["prediction"] == 1 
                      else "✅ Lower risk detected. Maintain healthy lifestyle."
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})

@app.route('/visualization')
def visualization():
    """Page showing model performance visualization"""
    return render_template('visualization.html')

@app.route('/generate_chart')
def generate_chart():
    """
    Generate model performance charts
    Returns base64 encoded images for web display
    """
    try:
        # Load the dataset for visualization
        df = pd.read_csv("heart.csv")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Heart Disease Dataset Analysis', fontsize=16, fontweight='bold')
        
        # Chart 1: Age distribution by target
        axes[0, 0].hist([df[df['target'] == 0]['age'], df[df['target'] == 1]['age']], 
                       bins=20, alpha=0.7, label=['No Disease', 'Disease'], color=['lightblue', 'lightcoral'])
        axes[0, 0].set_title('Age Distribution by Heart Disease')
        axes[0, 0].set_xlabel('Age')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Chart 2: Chest pain types
        cp_counts = df['cp'].value_counts().sort_index()
        axes[0, 1].bar(range(len(cp_counts)), cp_counts.values, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
        axes[0, 1].set_title('Distribution of Chest Pain Types')
        axes[0, 1].set_xlabel('Chest Pain Type (0-3)')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].set_xticks(range(len(cp_counts)))
        axes[0, 1].grid(True, alpha=0.3)
        
        # Chart 3: Heart rate vs Age colored by target
        scatter = axes[1, 0].scatter(df['age'], df['thalach'], c=df['target'], 
                                   cmap='coolwarm', alpha=0.6)
        axes[1, 0].set_title('Max Heart Rate vs Age')
        axes[1, 0].set_xlabel('Age')
        axes[1, 0].set_ylabel('Max Heart Rate')
        plt.colorbar(scatter, ax=axes[1, 0], label='Heart Disease')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Chart 4: Target distribution
        target_counts = df['target'].value_counts()
        wedges, texts, autotexts = axes[1, 1].pie(target_counts.values, 
                                                 labels=['No Disease', 'Disease'],
                                                 autopct='%1.1f%%',
                                                 colors=['lightblue', 'lightcoral'],
                                                 startangle=90)
        axes[1, 1].set_title('Heart Disease Distribution')
        
        # Adjust layout
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({"chart": img_base64})
        
    except Exception as e:
        return jsonify({"error": f"Error generating chart: {str(e)}"})

@app.route('/about')
def about():
    """About page with model information"""
    return render_template('about.html')

if __name__ == '__main__':
    # Check if required files exist
    required_files = ["heart_model.pkl", "scaler.pkl", "heart.csv"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️ Missing files: {missing_files}")
        print("Please run heart_detector.py first to generate model files!")
    else:
        print("🚀 Starting Heart Disease Prediction Web App...")
        print("📊 Access the app at: http://localhost:5000")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)