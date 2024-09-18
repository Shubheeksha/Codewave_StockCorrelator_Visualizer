# Stock Market Analysis Dashboard

This project is a Streamlit-based web application that provides stock market analysis tools, including correlation analysis, price forecasting, and sentiment analysis for selected stocks.

## Features

- Compare two stocks from a predefined list of major companies
- Visualize stock prices and their correlation over time
- Perform basic sentiment analysis
- Calculate risk metrics
- Forecast future stock prices using linear regression

## Installation

1. Clone this repository:
   ```
   https://github.com/Shubheeksha/Codewave_StockCorrelator_Visualizer.git
   cd stock-market-analysis
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:

```
streamlit run app/main.py
```

Navigate to the provided local URL in your web browser to use the application.

## Project Structure

```
stock_market_analysis/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data_fetcher.py
│   ├── analysis.py
│   └── visualization.py
│
├── config/
│   └── constants.py
│
├── requirements.txt
│
└── README.md
```

- `app/main.py`: Contains the Streamlit app and main function
- `app/data_fetcher.py`: Handles fetching stock data
- `app/analysis.py`: Includes analysis functions (correlation, forecasting, sentiment, risk)
- `app/visualization.py`: Contains functions for creating visualizations
- `config/constants.py`: Stores configuration constants like the list of stock tickers
- `requirements.txt`: Lists all Python dependencies
- `README.md`: Provides project information and setup instructions

## Dependencies

- streamlit
- pandas
- numpy
- yfinance
- matplotlib
- scikit-learn
- textblob
- seaborn

## Note

This project uses placeholder sentiment analysis. In a real-world scenario, you would need to implement a more sophisticated sentiment analysis system using actual news or social media data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.