import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[['Close']]
    df['Return'] = df['Close'].pct_change()
    df.dropna(inplace=True)
    return df

def forecast_future_prices(df, years_to_forecast):
    average_daily_return = df['Return'].mean()
    average_annual_return = average_daily_return * 252
    current_price = df['Close'][-1]
    future_prices = [current_price]
    for i in range(years_to_forecast):
        future_price = future_prices[-1] * (1 + average_annual_return)
        future_prices.append(future_price)
    future_dates = pd.date_range(start=df.index[-1], periods=years_to_forecast + 1, freq='Y')
    future_df = pd.DataFrame({'Close': future_prices}, index=future_dates)
    return future_df, average_annual_return

# Parameters
start_date = '2000-01-01'
end_date = '2023-12-31'
years_to_forecast = 5

# Get data for Coca-Cola
ko_df = get_stock_data('KO', start_date, end_date)
ko_future_df, ko_average_annual_return = forecast_future_prices(ko_df, years_to_forecast)

# Get data for PepsiCo
pep_df = get_stock_data('PEP', start_date, end_date)
pep_future_df, pep_average_annual_return = forecast_future_prices(pep_df, years_to_forecast)

# Plot both historical and predicted prices
plt.figure(figsize=(12, 6))
plt.plot(ko_df['Close'], label='KO Historical Prices')
plt.plot(ko_future_df['Close'], label='KO Predicted Prices', linestyle='--')
plt.plot(pep_df['Close'], label='PEP Historical Prices')
plt.plot(pep_future_df['Close'], label='PEP Predicted Prices', linestyle='--')
plt.title('Coca-Cola (KO) vs PepsiCo (PEP) Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend()
plt.show()