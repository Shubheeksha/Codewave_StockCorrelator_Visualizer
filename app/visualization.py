import matplotlib.pyplot as plt

def visualize_correlation(stock1, stock2, ticker1, ticker2):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Ensure data is sorted by index (date)
    stock1 = stock1.sort_index()
    stock2 = stock2.sort_index()
    
    # Plot stock prices
    ax1.plot(stock1.index, stock1.values, label=ticker1)
    ax1.plot(stock2.index, stock2.values, label=ticker2)
    ax1.set_title(f"Stock Prices: {ticker1} vs {ticker2}")
    ax1.legend()
    
    # Calculate and plot rolling correlation
    rolling_corr = stock1.rolling(window=30).corr(stock2)
    ax2.plot(rolling_corr.index, rolling_corr.values, label='Rolling Correlation')
    ax2.set_title(f"30-Day Rolling Correlation between {ticker1} and {ticker2}")
    
    # Color-code correlation strength
    for i in range(len(rolling_corr) - 1):
        if rolling_corr.iloc[i] > 0.7:
            ax2.axvspan(rolling_corr.index[i], rolling_corr.index[i+1], facecolor='green', alpha=0.1)
        elif rolling_corr.iloc[i] < 0.3:
            ax2.axvspan(rolling_corr.index[i], rolling_corr.index[i+1], facecolor='red', alpha=0.1)
    
    # Make sure layout is tight to avoid overlapping
    plt.tight_layout()
    return fig
