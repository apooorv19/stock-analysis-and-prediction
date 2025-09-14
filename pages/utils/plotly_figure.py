import plotly.graph_objects as go
import dateutil
import datetime
import pandas as pd

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    string_df = dataframe.astype(str)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b></b>"] + [f"<b>{col}</b>" for col in string_df.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35
        ),
        cells=dict(
            values=[
                [str(idx) for idx in string_df.index]  # show actual index (Market Cap, Beta, ...)
            ] + [
                string_df[col].tolist() for col in string_df.columns
            ],
            fill_color=[[rowOddColor, rowEvenColor] * ((len(string_df) // 2) + 1)],
            align='left',
            line_color='white',
            font=dict(color='black', size=15)
        ))
    ])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1).strftime('%Y-%m-%d')
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                           mode='lines',
                           name='Open', line=dict(width=2, color='#5ab7ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                           mode='lines',
                           name='Close', line=dict(width=2, color='black')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                           mode='lines', name='High', line=dict(width=2, color='#0078ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                           mode='lines', name='Low', line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(height=500, margin=dict(l=0, r=20, t=0, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', legend=dict(
        yanchor="top",
        xanchor="right"
    ))

    return fig


def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                                 open=dataframe['Open'], high=dataframe['High'],
                                 low=dataframe['Low'], close=dataframe['Close']))

    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white',
                      paper_bgcolor='#e1efff')

    return fig

def RSI(dataframe, num_period):
    # Calculate price change
    delta = dataframe['Close'].diff()

    # Get gains (positive changes) and losses (negative changes)
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate exponential moving average for gains and losses over a 14-day period
    period = 14
    avg_gain = gains.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = losses.ewm(com=period - 1, min_periods=period).mean()

    # Calculate Relative Strength (RS) and Relative Strength Index (RSI)
    rs = avg_gain / avg_loss
    dataframe['RSI'] = 100 - (100 / (1 + rs))

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['RSI'],
        marker_color='orange',
        line=dict(width=2, color='orange'),
        name='RSI'
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70] * len(dataframe),
        name='Overbought',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30] * len(dataframe),
        fill='tonexty',
        name='Oversold',
        marker_color='#79da84',
        line=dict(width=2, color='#79da84', dash='dash')
    ))

    fig.update_layout(
        yaxis_range=[0, 100],
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def Moving_average(dataframe, num_period):
    # Calculate the 50-period Simple Moving Average (SMA)
    dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close', line=dict(width=2, color='black')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict(width=2, color='#0078ff')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low', line=dict(width=2, color='red')))

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', name='SMA 50', line=dict(width=2, color='purple')))

    fig.update_xaxes(rangeslider_visible=True)

    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff',
                      legend=dict(yanchor="top", xanchor="right"))

    return fig


def MACD(dataframe, num_period):
    # Calculate the 12-period and 26-period EMAs
    ema_12 = dataframe['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = dataframe['Close'].ewm(span=26, adjust=False).mean()

    # Calculate the MACD line
    dataframe['MACD'] = ema_12 - ema_26

    # Calculate the Signal line (9-period EMA of the MACD line)
    dataframe['MACD Signal'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()

    # Calculate the MACD Histogram
    dataframe['MACD Hist'] = dataframe['MACD'] - dataframe['MACD Signal']

    # Filter data based on the selected period
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],
        name='MACD',
        marker_color='orange',
        line=dict(width=2, color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],
        name='MACD Signal',
        marker_color='red',
        line=dict(width=2, color='red', dash='dash')
    ))

    # Add the MACD Histogram as a bar chart
    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD Hist'],
        name='MACD Hist',
        marker_color=['green' if val >= 0 else 'red' for val in dataframe['MACD Hist']]
    ))

    fig.update_layout(
        height=200,
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h",
                    yanchor="top",
                    xanchor="right",
                    y=1.02,
                    x=1)
    )

    return fig

def Moving_average_forecast(forecast_data):
    """
    Creates a plot showing historical close prices and the 30-day forecast.

    Args:
        forecast_data (pd.DataFrame): A DataFrame containing the combined historical
                                      and forecasted 'Close' prices, with a DatetimeIndex.
                                      The last 30 rows are assumed to be the forecast.
    """
    # Define the split point. The forecast is the last 30 days.
    split_point = -30

    # Isolate the historical data (all data except the last 30 points)
    historical_data = forecast_data.iloc[:split_point]

    # Isolate the forecast data. We start from one point before the split
    # to ensure the red and black lines are connected seamlessly.
    future_data = forecast_data.iloc[split_point-1:]

    fig = go.Figure()

    # Trace 1: Historical Close Price (black line)
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='black')
    ))

    # Trace 2: Future Forecasted Price (red line)
    fig.add_trace(go.Scatter(
        x=future_data.index,
        y=future_data['Close'],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))

    # Add a range slider for better navigation
    fig.update_xaxes(rangeslider_visible=True)

    # Update layout for a clean appearance
    fig.update_layout(
        title="30-Day Stock Price Forecast",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='white',
        paper_bgcolor='#e1efff',
        legend=dict(
            yanchor="top",
            xanchor="right"
        )
    )

    return fig