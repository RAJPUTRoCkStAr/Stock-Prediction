import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import yfinance as yf
from streamlit_lottie import st_lottie
from lotti import lottie_predaccu
def pred():
    col9,col10 = st.columns(2)
    with col9:
        st.write("lets make prediction")
    with col10:
        lottie_predaccu
        map = st_lottie(lottie_predaccu,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)
    st.title("lets make a prediction")
    def fetch_historical_data(symbol, period):
        return yf.download(symbol, period=period)
    st.title('Stock Price Prediction')
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL):', 'AAPL')
    period = st.selectbox('Select Period:', ['1mo', '3mo', '6mo', '1y', '2y'], index=3)
    data = fetch_historical_data(symbol, period)
    st.subheader('Historical Stock Prices')
    st.line_chart(data['Close'])
    future_period = st.selectbox('Select Future Period:', ['1mo', '3mo', '6mo', '1y', '2y'], index=3)
    future_period_mapping = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365, '2y': 730}
    future_days = future_period_mapping[future_period]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(np.array(data['Close']).reshape(-1, 1))
    sequence_length = 50
    X, y = [], []
    for i in range(len(scaled_data) - sequence_length - 1):
        X.append(scaled_data[i:(i + sequence_length), 0])
        y.append(scaled_data[i + sequence_length, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32)
    inputs = scaled_data[-sequence_length:]
    future_predictions = []
    for i in range(future_days):
        inputs = inputs.reshape(1, -1)
        inputs = np.expand_dims(inputs, axis=2)
        future_price = model.predict(inputs)
        future_predictions.append(future_price[0][0])
        inputs = np.roll(inputs, -1)
        inputs[-1] = future_price
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=future_days)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price'))
    fig.add_trace(go.Scatter(x=future_dates, y=future_predictions.flatten(), mode='lines', name='Predicted Price'))
    fig.update_layout(title=f'Future Stock Price Prediction for {symbol}', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)
