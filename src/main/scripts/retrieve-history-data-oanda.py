import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd

# Define API endpoint
api_endpoint = 'https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles'

# Define API parameters
params = {
    'granularity': 'D',
    'count': 100,
    'price': 'M',
}

# Define API headers
headers = {
    'Authorization': 'Bearer',
}

# Send request to API
response = requests.get(api_endpoint, params=params, headers=headers)

# Extract data from response
data = response.json()['candles']

# Open CSV file for writing
with open('oanda_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['time', 'open', 'high', 'low', 'close'])

    # Write data rows
    for candle in data:
        time = candle['time']
        open_price = candle['mid']['o']
        high_price = candle['mid']['h']
        low_price = candle['mid']['l']
        close_price = candle['mid']['c']
        writer.writerow([time, open_price, high_price, low_price, close_price])

# Read in the CSV file
df = pd.read_csv('oanda_data.csv')

# Convert the 'time' column to a datetime object
df['time'] = pd.to_datetime(df['time'])

# Create the chart
fig, ax = plt.subplots()
ax.plot(df['time'], df['close'])
ax.set_xlabel('Time')
ax.set_ylabel('Close Price')
ax.set_title('EUR/USD Historical Close Prices')

# Show the chart
plt.show()