import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

# Load the data from the CSV file
data = pd.read_csv('src/main/test_data/stock_data.csv')

# Convert the 'Date' column to a datetime object and set it as the index
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Define the number of past days to use for predicting the future price
lookback = 60

# Create a window of the last 'lookback' days and convert the data to numpy arrays
X = data[-lookback:].values
y = data['Close'][-lookback:].values

# Scale the data to be between 0 and 1
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = scaler.fit_transform(y.reshape(-1,1))

# Reshape the data to be 3-dimensional
X_reshaped = np.reshape(X_scaled, (X_scaled.shape[0], X_scaled.shape[1], 1))

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_reshaped.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_reshaped, y_scaled, epochs=100, batch_size=32)

# Make predictions
X_test = np.array(data[-lookback+1:].values)
X_test_scaled = scaler.transform(X_test)
X_test_reshaped = np.reshape(X_test_scaled, (X_test_scaled.shape[0], X_test_scaled.shape[1], 1))
y_pred_scaled = model.predict(X_test_reshaped)
y_pred = scaler.inverse_transform(y_pred_scaled)

# Plot the predictions
import matplotlib.pyplot as plt
plt.plot(data.index[-lookback+1:], data['Close'][-lookback+1:], label='Actual Price')
plt.plot(data.index[-lookback+1:], y_pred, label='Predicted Price')
plt.legend()
plt.show()