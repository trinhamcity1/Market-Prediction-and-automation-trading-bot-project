import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load data from CSV file
data = pd.read_csv('oanda_data.csv')

# Preprocess data
x = data.iloc[:, 1:-1].values
y = data.iloc[:, -1].values

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Create and compile the model
model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=x_train.shape[1]))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Train the model
model.fit(x_train, y_train, epochs=50, batch_size=32, verbose=1)

# Evaluate the model
loss = model.evaluate(x_test, y_test, verbose=0)
print(f'Test loss: {loss}')

# Make predictions
y_pred = model.predict(x_test)

# Print example prediction
print(f'Prediction: {y_pred[0]}')