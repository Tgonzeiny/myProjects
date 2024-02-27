#Import necessary libraries
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import yfinance as yf

#Fetches stock data in the given dates
stockSymbol = 'TSLA'
startDate = '2023-01-01'
endDate = '2024-02-26'
yf.pdr_override()
df = web.DataReader(stockSymbol,startDate, endDate)

#Data exploration
print(df.head())
df['Close'].plot(title=f'{stockSymbol}  Stock Closing Price')
plt.show()

#Prepares the data for modeling and uses only the closing price to predict the future
X = df[['Close']]
y = df['Close'].shift(-1) #Predicts the enxt day closing price

X = X[:-1] # Removes the last row
y = y.dropna() #Removes the last value

#Splits the data
X_Train, X_Test, y_Train, y_Test = train_test_split(X, y, test_size=0.05)

#Builds the model for regression
model = LinearRegression()
model.fit(X_Train, y_Train)

#Prediction model
y_pred = model.predict(X_Test)

#Evaluation
mse = mean_squared_error(y_Test, y_pred)
print(f'MSE: {mse}')

#Visualization
print(y_pred)
plt.figure(figsize=(10,6))
plt.plot(y_Test.index, y_Test, label = 'Actual Price')
plt.plot(y_Test.index,  y_pred, label='Predicted Price', color = 'red')
plt.title(f'{stockSymbol} Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price')
plt.ylim()
plt.legend()
plt.show()



