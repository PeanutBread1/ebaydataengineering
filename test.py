import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Step 1: Load and Prepare the Data
# Assuming 'date' is your date column and 'price' is your price column
data = pd.read_csv('listings.csv', parse_dates=['date'], index_col='date')
data.sort_index(inplace=True)

# Step 2: Visualize the Data
# Plotting the 'price' column
data['price'].plot()  # Ensure 'price' matches your CSV column name for prices
plt.title('LEGO Set Prices Over Time')
plt.ylabel('Price')
plt.xlabel('Date')
plt.show()

# Step 3: Time Series Forecasting with ARIMA
# Define and fit the model
# The ARIMA model will be applied on the 'price' column
model = ARIMA(data['price'], order=(1, 1, 1))  # Adjust the order (p,d,q) as necessary
model_fit = model.fit()

# Print the summary
print(model_fit.summary())

# Step 4: Make Predictions
# Forecast the next 5 data points
forecast = model_fit.forecast(steps=5)
print(forecast)
