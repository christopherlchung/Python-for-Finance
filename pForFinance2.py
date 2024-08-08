import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = 'MSFT'
start_date = '2000-01-01'
end_date = '2023-12-31'

df = yf.download(ticker, start=start_date, end=end_date)
df = df[['Close']]

df['Return'] = df['Close'].pct_change()

average_daily_return = df['Return'].mean()
average_annual_return = average_daily_return * 252
df.dropna(inplace=True)
print(df.head())

current_price = df['Close'][-1]
future_prices = [current_price]

years_to_forecast = 5

for i in range(years_to_forecast):
    future_price = future_prices[-1] * (1 + average_annual_return)
    future_prices.append(future_price)

# Now we need to create a seperate DataFrame to plot the forecasted price data 
# (which will be plotted on the same graph with historical data)

future_dates = pd.date_range(start=df.index[-1], periods=years_to_forecast+1, freq='Y')
future_df = pd.DataFrame({'Close': future_prices}, index=future_dates)

plt.plot(df['Close'], label='Historical Prices')
plt.plot(future_df['Close'], label='Predicted Prices', linestyle='--')
plt.title('Microsoft (MSFT) Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend()
plt.show()