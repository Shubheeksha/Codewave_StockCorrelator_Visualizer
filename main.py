import streamlit as st
import pandas as pd
import networkx as nx
import numpy as np
from app.data_fetcher import fetch_stock_data
from app.analysis import calculate_correlation, time_series_forecast, sentiment_analysis, risk_metric
from app.visualization import visualize_correlation
from config.constants import tickers
import matplotlib.pyplot as plt

def calculate_eigenvector_centrality(correlation_matrix, stock_names):
    # Create a graph from the correlation matrix
    G = nx.Graph()

    # Add edges with correlation values as weights
    for i in range(len(stock_names)):
        for j in range(i + 1, len(stock_names)):
            if i != j:
                G.add_edge(stock_names[i], stock_names[j], weight=correlation_matrix[i, j])
    
    # Compute eigenvector centrality
    centrality = nx.eigenvector_centrality_numpy(G, weight='weight')
    
    return centrality

def main():
    st.title("Stock Market Analysis Dashboard")

    if 'show_forecasting' not in st.session_state:
        st.session_state.show_forecasting = False
    if 'show_centrality' not in st.session_state:
        st.session_state.show_centrality = False
        
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
            forecast_months = st.number_input("Number of months to forecast:", min_value=1, max_value=6, value=3)
        
            # Calculate and display forecasts
            most_recent_date = data1.index[-1]
            forecast_periods = forecast_months * 30  # Approximate number of days to forecast
            
            # Forecasting from the most recent date in the data
            forecast1 = time_series_forecast(data1, forecast_periods)
            forecast2 = time_series_forecast(data2, forecast_periods)

            future_dates = pd.date_range(start=most_recent_date + pd.Timedelta(days=1), periods=forecast_periods)

            # Update the historical data to start from 2024
            start_date_2024 = pd.to_datetime('2024-01-01')
            if data1.index.tz is not None:  # Check if timezone is present
                start_date_2024 = start_date_2024.tz_localize(data1.index.tz)
            historical_data1 = data1[data1.index >= start_date_2024]
            historical_data2 = data2[data2.index >= start_date_2024]

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(historical_data1.index, historical_data1.values, label=f'{stock1} Historical')
            ax.plot(historical_data2.index, historical_data2.values, label=f'{stock2} Historical')
       
            ax.plot(future_dates, forecast1, label=f'{stock1} Forecast', linestyle='--')
            ax.plot(future_dates, forecast2, label=f'{stock2} Forecast', linestyle='--')
            ax.set_title("Stock Price Forecast")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
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
    
    if st.button("Toggle Eigenvector Centrality", key="show_centrality_button"):
        st.session_state.show_centrality = not st.session_state.show_centrality

    # Show Eigenvector Centrality section only if toggled
    if st.session_state.show_centrality:
        st.sidebar.subheader("Eigenvector Centrality for Stock Network")
        
        # Fetch data for all stocks
        stock_data = {}
        for stock in tickers:
            data = fetch_stock_data(stock, start_date, end_date)
            if not data.empty:
                stock_data[stock] = data

        if len(stock_data) > 1:
            st.header("Eigenvector Centrality Analysis")

            # Calculate correlation matrix
            stock_prices = pd.DataFrame({stock: data for stock, data in stock_data.items()})

            correlation_matrix = stock_prices.corr().values
            stock_names = stock_prices.columns.tolist()

            # Calculate eigenvector centrality
            centrality = calculate_eigenvector_centrality(correlation_matrix, stock_names)

            # Sort and display centrality results
            centrality_sorted = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            st.subheader("Most Influential Stocks (by Eigenvector Centrality)")
            for stock, score in centrality_sorted:
                st.write(f"{stock}: {score:.4f}")

            # Optional: Visualize the correlation matrix as a heatmap
            st.subheader("Correlation Matrix Heatmap")
            fig, ax = plt.subplots(figsize=(10, 8))
            cax = ax.matshow(correlation_matrix, cmap='coolwarm')
            fig.colorbar(cax)
            ax.set_xticks(np.arange(len(stock_names)))
            ax.set_yticks(np.arange(len(stock_names)))
            ax.set_xticklabels(stock_names, rotation=90)
            ax.set_yticklabels(stock_names)
            st.pyplot(fig)
        else:
            st.write("Not enough stock data available for the selected date range.")
if __name__ == "__main__":
    main()
