"""
Performance Evaluation Module
-----------------------------

This module, `Performance`, is designed to evaluate the performance of trading strategies. 
It takes a portfolio as a pandas DataFrame, which includes time series data of returns, 
holdings, valuations, and profit and loss (PnL).

Your task is to implement various financial performance metrics within this class. 
The portfolio DataFrame will be your primary input. This can be generated from 
the derived implementation of the backtest.portfolio.Portfolio class and accessing
the result from the backtest_strategy() method.

Guidelines for Implementation:
1. Initialize the class with the portfolio DataFrame.
2. Implement methods to calculate the following metrics:
   - Alpha Ratio: Measure of active return on an investment relative to a suitable market index.
   - Total Profit and Loss: The total net profit or loss of the portfolio over a period.
   - Sharpe Ratio: Measures the performance of an investment compared to a risk-free asset, 
                   after adjusting for its risk.
   - Sortino Ratio: Similar to the Sharpe Ratio but penalizes only those returns falling below 
                    a user-defined target or required rate of return.
   - (Feel free to add more metrics like Beta, Maximum Drawdown, Annualized Return, etc.)
3. Write methods to generate visualizations of the key metrics of the given strategy.

Example:
class Performance:
    def __init__(self, portfolio_df):
        # Initialize with portfolio DataFrame
        self.portfolio = portfolio_df

    def alpha_ratio(self):
        # Implement alpha ratio calculation
        pass

    def total_pnl(self):
        # Implement total profit and loss calculation
        pass

    # Add more methods for other metrics

Remember, each method should be well-documented, explaining what it calculates, the formula used, 
and any assumptions made. Comments should be clear and concise.

The goal of this exercise is to familiarize you with the key performance indicators used in quantitative 
finance and to give you hands-on experience in implementing these metrics.

Happy coding!
"""
