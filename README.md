# Moving Average Crossover Strategy

## Introduction

This project, Moving Average Crossover Strategy, is a comprehensive tool for implementing and analyzing financial trading strategies, specifically focusing on the Moving Average Crossover Strategy. It is designed for educational purposes, providing a hands-on experience in financial data processing, strategy implementation, and performance analysis.

## Features

- **Data Collection**: Module for downloading and preprocessing financial market data.
- **Strategy Implementation**: Base classes for developing trading strategies, with a specific implementation of the Moving Average Crossover Strategy.
- **Backtesting**: Tools for simulating trading strategies on historical data to assess their effectiveness.
- **Performance Analysis**: Comprehensive analysis of strategy performance including metrics like Sharpe ratio, Sortino ratio, and Alpha ratio.

## Installation

To set up this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/QuantSquad/MovingAverageCrossoverStrategy
cd MovingAverageCrossoverStrategy
pip3 install -r requirements.txt
```

## Usage

The project includes a Jupyter Notebook (main.ipynb) for a quick start and interactive experience with the code. To use the project modules:

1. Import the necessary classes from the `src` folder.
2. Use the `src.data.data_colletion.py` to analyze raw financial data.
3. Implement or use existing strategies in `src.strats`.
4. Backtest the strategies using classes in `src.backtest`.
5. Analyze the performance with the `src.backtest.performance` module (after you implement it!).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
