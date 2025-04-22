from flask import Flask, render_template, request
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extract input features from the form
            features = [
                float(request.form.get(feat)) for feat in [
                    'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
                    'waterfront', 'view', 'condition', 'grade', 'sqft_above',
                    'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat',
                    'long', 'sqft_living15', 'sqft_lot15', 'House_Age'
                ]
            ]
            # Optional: add 'id' and 'date' if the model uses them
            # But usually these are dropped
            prediction = model.predict([features])[0]

            # Convert back from log(price) if necessary
            predicted_price = np.exp(prediction)

            return render_template('result.html', prediction=round(predicted_price, 2))
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
