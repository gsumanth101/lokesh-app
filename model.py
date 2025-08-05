import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load sample soil data
data = pd.DataFrame({
    'temperature': [25, 30, 22, 27, 31],
    'humidity': [50, 60, 65, 70, 55],
    'N': [10, 20, 15, 30, 25],
    'P': [15, 20, 25, 10, 20],
    'K': [20, 30, 25, 35, 40],
    'pH': [6.5, 6.8, 7.1, 6.0, 6.3],
    'rainfall': [200, 150, 180, 100, 300],
    'crop': ['wheat', 'rice', 'maize', 'barley', 'millet']
})

# Features and target
X = data[['temperature', 'humidity', 'N', 'P', 'K', 'pH', 'rainfall']]
y = data['crop']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save the model
with open('crop_recommendation_model.pkl', 'wb') as f:
    pickle.dump(model, f)

