import datetime
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
from pages.utils import CAPM_logic
import numpy as np

st.set_page_config(page_title="CAPM Calculator",
                   page_icon="chart_with_upwards_trend",
                   layout="wide")

st.title("Capital Asset Pricing Model")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

col1, col2 = st.columns([1, 1])

with col1:
    stocks_list = st.multiselect("Choose stocks", ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
                                ['TSLA', 'AAPL', 'AMZN', 'GOOGL'])
with col2:
    year = st.number_input("Number of years", 1, 10)

# --- S&P 500 Data Fetching ---
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    SP500 = web.DataReader(["sp500"], "fred", start, end)
except Exception as e:
    st.error(f"Failed to download S&P 500 data: {e}")
    st.stop()

# --- Stock Data Fetching ---
stocks_df = pd.DataFrame()
for stock in stocks_list:
    try:
        data = yf.download(stock, period=f'{year}y')
        if data.empty:
            st.warning(f"No data found for {stock}. Skipping.")
            continue
        stocks_df[f'{stock}'] = data['Close']
    except Exception as e:
        st.warning(f"Could not download data for {stock}. Skipping. Error: {e}")

# --- Check if any stock data was successfully downloaded ---
if stocks_df.empty:
    st.error("Could not download any valid stock data. Please check the tickers or try again later.")
    st.stop()

stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns = ['Date', 'sp500']

stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

try:
    stocks_df = pd.merge(stocks_df, SP500, how='inner', on='Date')
except Exception as e:
    st.error(f"An error occurred during data merging: {e}")
    st.stop()

if stocks_df.empty:
    st.error("Data could not be merged. There might be no overlapping dates between stock data and S&P 500 data.")
    st.stop()

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('### DataFrame Head')
    st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
    st.markdown('### DataFrame Tail')
    st.dataframe(stocks_df.tail(), use_container_width=True)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Price of all the stocks")
    st.plotly_chart(CAPM_logic.interactive_plot(stocks_df))
with col2:
    st.markdown("### Price of all the stocks (After Normalizing)")
    st.plotly_chart(CAPM_logic.interactive_plot(CAPM_logic.normalize(stocks_df)))

stocks_daily_return = CAPM_logic.daily_return(stocks_df)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

beta = {}
alpha = {}

for i in stocks_daily_return.columns:
    if i != 'Date' and i != 'sp500':
        try:
            b, a = CAPM_logic.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a
        except Exception as e:
            st.warning(f"Could not calculate Beta/Alpha for {i}. Skipping. Error: {e}")

if not beta:
    st.error("Beta could not be calculated for any of the selected stocks.")
    st.stop()

beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

with col1:
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width=True)

rf = 0.0
rm = stocks_daily_return['sp500'].mean() * 252

return_df = pd.DataFrame()
return_value = []

valid_stocks = list(beta.keys())

for stock in valid_stocks:
    # --- CAPM Calculation ---
    expected_return = rf + (beta[stock] * (rm - rf))
    return_value.append(str(round(expected_return, 2)))

return_df['Stock'] = valid_stocks
return_df['Return Value'] = return_value

with col2:
    st.markdown('### Calculated Return using CAPM')
    st.dataframe(return_df, use_container_width=True)