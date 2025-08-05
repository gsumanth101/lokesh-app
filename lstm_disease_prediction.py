import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Load dataset
data = pd.read_csv('early_crop_disease_dataset_full.csv')

# Preprocess dataset
numerical_features = ['temperature', 'humidity', 'rainfall', 'soil_pH', 'nitrogen', 'phosphorus', 'potassium']
categorical_features = ['crop_stage', 'crop_type']

data[numerical_features] = StandardScaler().fit_transform(data[numerical_features])

encoder = OneHotEncoder(sparse=False)
encoded_cat = encoder.fit_transform(data[categorical_features])
encoded_cat_df = pd.DataFrame(encoded_cat, columns=encoder.get_feature_names_out(categorical_features))

processed_data = pd.concat([data[numerical_features], encoded_cat_df, data['disease_label']], axis=1)

# Create sliding windows
sequence_length = 7
X, y = [], []
for i in range(len(processed_data) - sequence_length + 1):
    X.append(processed_data.iloc[i:i+sequence_length].drop('disease_label', axis=1).values)
    y.append(processed_data.iloc[i:i+sequence_length]['disease_label'].values[-1])

X, y = np.array(X), np.array(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define Dataset class
class CropDiseaseDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)
    def __len__(self):
        return len(self.y)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_dataset = CropDiseaseDataset(X_train, y_train)
test_dataset = CropDiseaseDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Define LSTM Model
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        device = x.device
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h_0, c_0))
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        return out

# Initialize and train model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
input_size = X_train.shape[2]
hidden_size = 64
num_layers = 1
output_size = 1

model = LSTMModel(input_size, hidden_size, num_layers, output_size)
model = model.to(device)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 5
model.train()
for epoch in range(num_epochs):
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs.squeeze(), y_batch)
        loss.backward()
        optimizer.step()

# Evaluation
model.eval()
all_preds = []
all_labels = []
with torch.no_grad():
    for X_batch, y_batch in test_loader:
        X_batch = X_batch.to(device)
        outputs = model(X_batch)
        preds = torch.round(torch.sigmoid(outputs.squeeze().cpu()))
        all_preds.extend(preds.numpy())
        all_labels.extend(y_batch.numpy())

accuracy = accuracy_score(all_labels, all_preds)
f1 = f1_score(all_labels, all_preds)
conf_matrix = confusion_matrix(all_labels, all_preds)

# Output results
print("Accuracy:", accuracy)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)

# Save model
torch.save(model.state_dict(), 'disease_prediction_model.pt')
