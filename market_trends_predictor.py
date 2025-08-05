import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset
file_path = 'C:\\Users\\SAI PRUDHVI\\Downloads\\unite\\Inf\\data\\markettrends.csv'
data = pd.read_csv(file_path)

# Feature selection
features = data[['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']]
target = data['Modal_x0020_Price']

# One-hot encode categorical features
encoder = OneHotEncoder(sparse=False)
features_encoded = encoder.fit_transform(features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_encoded, target, test_size=0.2, random_state=42)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Calculate mean squared error
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Saving the model
model_path = 'market_trends_model.pkl'
with open(model_path, 'wb') as model_file:
    import pickle
    pickle.dump(model, model_file)

print(f'Model saved to {model_path}')
