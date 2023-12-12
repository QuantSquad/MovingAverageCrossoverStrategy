"""
This module contains the class definition for the Strategy class, which serves as an abstract 
base class providing an interface for all derived trading strategies. Each derived strategy 
class is expected to implement its own signal generation method, tailored to the specifics 
of that strategy. Currently, this framework is designed to support strategies involving a 
single financial instrument.
"""

from abc import ABCMeta, abstractmethod
import pandas as pd

class Strategy(metaclass=ABCMeta):
    """
    The Strategy class is an abstract base class that outlines the structure for
    trading strategies. 

    Each derived class should implement its own method for generating trading signals
    based on specific strategy logic. The generated signals should be represented as a
    pandas DataFrame indexed by time, with each value indicating the trading action:
    1 for buy, -1 for sell, and 0 for hold.
    
    Note:
        - The current design supports strategies for single financial instruments.
        - Derived classes must implement the `generate_signals` method.
    """

    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        """
        Generates trading signals based on the strategy logic.

        Returns:
            pandas.DataFrame: A DataFrame with time-series index representing the
                              trading signals (1 for buy, -1 for sell, 0 for hold).
        Raises:
            NotImplementedError: If the method is not implemented in the derived class.
        """
        raise NotImplementedError("Strategy child class must implement generate_signals()")
