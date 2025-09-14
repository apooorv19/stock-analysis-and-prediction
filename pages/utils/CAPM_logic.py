import plotly.express as px
import numpy as np


def interactive_plot(df):
    # Specify the x and y axes explicitly
    # y=df.columns[1:] tells Plotly to use all columns *except* the first one ('Date') for the y-axis.
    fig = px.line(df, x='Date', y=df.columns[1:])

    # The rest of your styling
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, b=20, t=50),
        legend=dict(
            title_text='',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i][0]
    return df


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Function to calculate daily returns
# The correct and safe way to calculate daily returns
def daily_return(df):
    # Work on a copy of the price data, excluding the 'Date' column
    price_df = df.drop(columns='Date')

    # Use the built-in pct_change() function
    daily_returns = price_df.pct_change()

    # Multiply by 100 and fill the first row (which is NaN) with 0
    daily_returns_pct = daily_returns.fillna(0) * 100

    # Add the 'Date' column back to the start
    daily_returns_pct.insert(0, 'Date', df['Date'])

    return daily_returns_pct


# Function to calculate Beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean() * 252

    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)
    return b, a


