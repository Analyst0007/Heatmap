import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.title('Stock Returns Heatmap')

# User input for stock ticker
ticker = st.text_input('Enter Stock Ticker', 'AAPL')

# User input for period
period = st.selectbox('Select Period', ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'])

# Fetch data from Yahoo Finance
@st.cache_data
def get_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

data = get_data(ticker, period)

# Calculate monthly returns
data['Month'] = data.index.to_period('M')
monthly_returns = data.groupby('Month')['Close'].apply(lambda x: (x[-1] - x[0]) / x[0])

# Reshape the DataFrame for the heatmap
monthly_returns = monthly_returns.reset_index()
monthly_returns['Year'] = monthly_returns['Month'].dt.year
monthly_returns['Month'] = monthly_returns['Month'].dt.month
pivot_returns = monthly_returns.pivot(index='Year', columns='Month', values='Close')

# Create a heatmap
st.subheader('Monthly Returns Heatmap')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pivot_returns, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
st.pyplot(fig)
