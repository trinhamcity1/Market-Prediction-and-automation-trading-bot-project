import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd

# Define API endpoint
api_endpoint = 'https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles'

# Define API parameters

# 4H chart
params_4h = {
    'granularity': 'H4',
    'count': 24,
    'price': 'M'
}

# 1 day chart
params_1d = {
    'granularity': 'D',
    'count': 100,
    'price': 'M',
}

# Define API headers
headers = {
    'Authorization': 'Bearer be51236df75cf7c7cf698dcb7b1cb99a-a535de4d1e7dac37ba93d8d0a48b25ca',
}

# Send request to API
response = requests.get(api_endpoint, params=params_4h, headers=headers)

# Extract data from response
data = response.json()['candles']

# Open CSV file for writing
with open('src/main/test_data/oanda_data_4h.csv', 'w', newline='') as csvfile:
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
df = pd.read_csv('src/main/test_data/oanda_data_4h.csv')

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