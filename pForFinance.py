import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Collect Historical Data
ticker = 'KO'
start_date = '2000-01-01'
end_date = '2023-12-31'
df = yf.download(ticker, start=start_date, end=end_date)

# Step 2: Prepare the Data
df = df[['Close']]
df['Return'] = df['Close'].pct_change() # Creating new column 'Return' that takes percent change of 'Close'
df.dropna(inplace=True) # Remove missing values

print(df.head())

# Step 3: Calculate Historical Growth Rates
# Now that our historical data is prepared and ready for analysis, we can begin calculating 
# historical growth rates to help us project future growth rates.
# Let's start off by finding the average annual return of KO. To do this, we need
# to find the average daily return first, and then multiply by 252 (trading days / year).

average_daily_return = df['Return'].mean() # Defining/calculating average daily return by selecting 
# the 'Return' column and calculating mean using '.mean()'
average_annual_return = average_daily_return * 252
print(f"Average Annual Return: {average_annual_return * 100:.2f}%") # f-string, allowing us to embed expressions inside 
# string literals, converting return to decimal

# Step 4: Predicting Future Values
years_to_forecast = 5
# Now, after setting how many years to forecast into, we need an actual place or reference point to start with!
current_price = df['Close'][-1] # Defining 'current_price' as latest closing price, selecting the 'Close' column.
future_prices = [current_price] # Creating a new list called for future prices, but we start the list with the current price.
for i in range(years_to_forecast): # Looping through the number of years to forecast (for i in range(5) becomes [0, 1, 2, 3, 4])
    future_price = future_prices[-1] * (1 + average_annual_return) # Taking the latest/most recent value and multiplying by return rate
    future_prices.append(future_price) # Appending this new value into the overall future prices list.

# Step 5: Creating a Data Frame for Forecasted Prices
future_dates = pd.date_range(start=df.index[-1], periods=years_to_forecast+1, freq='Y') # pd.date_range() is a function in the pandas library that generates a range of dates.
# It takes several parameters, including start, periods, and freq.
# In this case, the future dates data frame is starting with the last index/row of our original data frame.
# Index in data frames are rows!!! index = rows
future_df = pd.DataFrame({'Close': future_prices}, index=future_dates)

plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Historical Prices')
plt.plot(future_df['Close'], label='Predicted Prices', linestyle='--')
plt.title('Coca-Cola (KO) Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend()
plt.show()

# Read pandas documentation!!!