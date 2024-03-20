import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

#load prep data
data = pd.read_csv('listings.csv', parse_dates=['date'], index_col='date')
data.sort_index(inplace=True)

#plot
data['price'].plot()  
plt.title('LEGO Set Prices Over Time')
plt.ylabel('Price')
plt.xlabel('Date')
plt.show()

#timeseries forcasting
model = ARIMA(data['price'], order=(1, 1, 1)) 
model_fit = model.fit()

print(model_fit.summary())

#next 5 data points
forecast = model_fit.forecast(steps=5)
print(forecast)
