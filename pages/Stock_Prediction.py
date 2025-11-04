import streamlit as st
import pandas as pd
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling, get_daily_returns, fit_garch_model
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="🔮",
    layout="wide",
)

st.title("Stock Prediction 🔮")
st.info("This tool uses an ARIMA model to forecast the next 30 days of a stock's closing price. Please note that this is a statistical forecast and not financial advice.")

ticker = st.text_input("Enter Stock Ticker", "AAPL").upper()

if ticker:
    try:
        with st.spinner(f"Running forecast for {ticker}... This may take a moment."):
            # --- Model Training ---
            close_price = get_data(ticker)
            if close_price.empty:
                st.error(f"Could not retrieve data for {ticker}. Please check the ticker symbol.")
                st.stop()

            # The model is trained on the smoothed, rolling average price
            rolling_price = get_rolling_mean(close_price)
            differencing_order = get_differencing_order(rolling_price)
            scaled_data, scaler = scaling(rolling_price)
            rmse = evaluate_model(scaled_data, differencing_order)

            st.subheader(f'Forecast for: {ticker}')
            st.write(f"**Model RMSE Score:** {rmse:.2f}")
            st.caption("Lower RMSE (Root Mean Squared Error) generally indicates a better model fit.")

            # --- Forecasting ---
            scaled_forecast_df = get_forecast(scaled_data, differencing_order)
            unscaled_forecast_values = inverse_scaling(scaler, scaled_forecast_df['Close'])

            # Create a clean DataFrame for the final forecast values
            forecast_df = pd.DataFrame(unscaled_forecast_values, index=scaled_forecast_df.index, columns=['Close'])

            # --- Display Forecast Data Table ---
            st.write("#### Forecast Data (Next 30 days)")
            st.plotly_chart(plotly_table(forecast_df.round(2)), use_container_width=True)
            
            # NEW GARCH IMPLEMENTATION FOR VOLATILITY (Module 4)
# --------------------------------------------------------------------------

            # 1. Prepare data (daily returns are required for GARCH)
            returns = get_daily_returns(close_price['Close'])

            # 2. Fit and forecast GARCH(1,1) model (p=1, q=1 are common starting points)
            volatility_forecast_df, garch_results = fit_garch_model(returns, p=1, q=1)

            # 3. Display GARCH Results (e.g., model parameters)
            st.write("### GARCH Model Results (Volatility Forecast)")
            st.write(f"**Model:** GARCH({garch_results.p}, {garch_results.q})")
            st.write(f"**Log-Likelihood:** {garch_results.loglikelihood:.4f}")
            st.write(f"**AIC/BIC:** {garch_results.aic:.2f} / {garch_results.bic:.2f}")

            # 4. Display Volatility Forecast Table
            st.write("#### Forecasted Volatility (Next 30 days)")
            # We use the existing plotly_table to display the volatility forecast
            st.plotly_chart(plotly_table(volatility_forecast_df.round(4)), use_container_width=True)

            # --- Display Forecast Chart ---
            # FIX: Plot the ORIGINAL historical close price, not the rolling average.
            # This makes the chart more intuitive and aligns with the legend.
            # Also, remove timezone info to prevent potential concatenation errors.
            close_price.index = close_price.index.tz_localize(None)
            combined_data_for_plot = pd.concat([close_price, forecast_df])
            st.plotly_chart(Moving_average_forecast(combined_data_for_plot.iloc[-200:]), use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred during model training or prediction: {e}")