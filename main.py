import streamlit as st
import pandas as pd
from app.data_fetcher import fetch_stock_data
from app.analysis import calculate_correlation, time_series_forecast, sentiment_analysis, risk_metric
from app.visualization import visualize_correlation
from config.constants import tickers
import matplotlib.pyplot as plt

def main():
    st.title("Stock Market Analysis Dashboard")

    if 'show_forecasting' not in st.session_state:
        st.session_state.show_forecasting = False

    # Sidebar for stock selection and date range
    st.sidebar.header("Select Stocks and Date Range")
    stock1 = st.sidebar.selectbox("Choose first stock:", tickers)
    stock2 = st.sidebar.selectbox("Choose second stock:", tickers, index=1)
    
    start_date = st.sidebar.date_input("Start date:", pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input("End date:", pd.to_datetime('today'))

    # Fetch stock data
    data1 = fetch_stock_data(stock1, start_date, end_date)
    data2 = fetch_stock_data(stock2, start_date, end_date)

    if not data1.empty and not data2.empty:
        # Display basic information
        st.header("Stock Information")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(stock1)
            st.write(f"Current Price: ${data1.iloc[-1]:.2f}")
            st.write(f"Risk Metric: {risk_metric(data1):.2f}")
            st.write(f"Sentiment: {sentiment_analysis(stock1):.2f}")
        with col2:
            st.subheader(stock2)
            st.write(f"Current Price: ${data2.iloc[-1]:.2f}")
            st.write(f"Risk Metric: {risk_metric(data2):.2f}")
            st.write(f"Sentiment: {sentiment_analysis(stock2):.2f}")

        # Correlation analysis
        st.header("Correlation Analysis")
        correlation = calculate_correlation(data1, data2)
        st.write(f"Correlation between {stock1} and {stock2}: {correlation:.2f}")
        
        # Visualization
        st.pyplot(visualize_correlation(data1, data2, stock1, stock2))
        
        if st.button("Show Forecasting", key="show_forecasting_button"):
            st.session_state.show_forecasting = not st.session_state.show_forecasting

        # Forecasting section (only visible when the button is toggled)
        if st.session_state.show_forecasting:
            st.header("Stock Price Forecasting")
            forecast_days = st.number_input("Number of days to forecast:", min_value=1, max_value=30, value=7)
        
            # Calculate and display forecasts
            forecast1 = time_series_forecast(data1, forecast_days)
            forecast2 = time_series_forecast(data2, forecast_days)

            future_dates = pd.date_range(start=data1.index[-1] + pd.Timedelta(days=1), periods=forecast_days)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data1.index, data1.values, label=f'{stock1} Historical')
            ax.plot(data2.index, data2.values, label=f'{stock2} Historical')
            ax.plot(future_dates, forecast1, label=f'{stock1} Forecast', linestyle='--')
            ax.plot(future_dates, forecast2, label=f'{stock2} Forecast', linestyle='--')
            ax.set_title("Stock Price Forecast")
            ax.legend()
            st.pyplot(fig)

            # Display forecasted prices
            st.subheader("Forecasted Prices")
            forecast_df = pd.DataFrame({
                'Date': future_dates,
                f'{stock1} Forecast': forecast1,
                f'{stock2} Forecast': forecast2
            })
            st.dataframe(forecast_df.set_index('Date'))

    else:
        st.write("No data available for the selected date range and stocks.")

if __name__ == "__main__":
    main()