"""
This module contains the class definition for the
InstrumentInfo class which collects and processes 
historical price information for a particular 
financial instrument
"""

from typing import Optional
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from utils.data_fetch_decorator import data_fetch_decorator


class InstrumentInfo:
    """
    The InstrumentInfo class is responsible for collecting and processing
    historical price data for a given financial instrument from a specified
    time range.

    Attributes:
        instrument (str) : The financial instrument (e.g., stock ticker) for which data is collected
        start_date (str) : The start date for the data collection in 'YYYY-MM-DD' format.
        end_date (str) : The end date for the data collection in 'YYYY-MM-DD' format.
        historical_data (pd.DataFrame) : The processed historical data.

    Methods:
        fetch_raw_data : Fetches the histical data of the instrument from yfinance
        process_data : Processes the raw data into a usable format.
        get_historical_data : Returns the processed historical data.

    Usage example:
        >>> AAPL = InstrumentInfo('AAPL', '2020-01-01', '2021-01-01')
        >>> AAPL_HISTORICAL_DATA = AAPL._get_historical_data()
        >>> print(AAPL_HISTORICAL_DATA.head())

    """

    def __init__(self, instrument: str, start_date: str, end_date: str) -> None:
        self.instrument = instrument
        self.start_date = start_date
        self.end_date = end_date
        self.historical_data = self._get_historical_data()

        self.earliest_available_date = None
        self.latest_available_date = None
        self._validate_inputs()

    def _validate_inputs(self):
        """
        Validates the inputs for the InstrumentInfo class.

        This method validates the instrument ticker symbol and the date range (start and end dates)
        for data collection. It ensures the ticker symbol is valid, the dates are in the correct
        format, and the start date is before the end date.

        Usage:
            This method is called internally by the __init__ method. It is not intended
            to be called directly.
        Raises:
            ValueError: If the start date is after or at the end date.
        Usage:
            This method is called internally by the __init__ method. It is not intended
            to be called directly.
        """
        self._validate_instrument()
        self._validate_date(self.start_date, "Start date")
        self._validate_date(self.end_date, "End date")

        if self.start_date >= self.end_date:
            raise ValueError("Start date must be earlier than end date.")

    def _validate_instrument(self):
        """
        Validates if the instrument (ticker symbol) exists using yfinance.

        This method uses yfinance to check if the provided ticker symbol
        corresponds to a financial instrument with available data.
        It determines the earliest and latest available data dates for the instrument.
        It raises an exception if the ticker is invalid or data is unavailable.

        Sets:
            self.earliest_available_date (datetime): The earliest available date with data for the
                                                     instrument.
            self.latest_available_date (datetime): The latest available date with data for the
                                                   instrument.
        Raises:
            ValueError: If the ticker symbol is not a string or not uppercase.
            ValueError: If the ticker symbol is invalid or has no date.
            ValueError: If there as an error validating the ticker.
        Usage:
            This method is called internally by the _validate_inputs method. It is not intended
            to be called directly.
        """
        if not isinstance(self.instrument, str) or not self.instrument.isupper():
            raise ValueError("Instrument must be a string in uppercase.")

        try:
            historical_data = yf.Ticker(self.instrument).history(period="max")
            if historical_data.empty:
                raise ValueError(
                    f"Ticker symbol '{self.instrument}' is invalid or has no data"
                )

            self.earliest_available_date = historical_data.index.min().to_pydatetime()
            self.latest_available_date = historical_data.index.max().to_pydatetime()

            if (
                    self.earliest_available_date.tzinfo is not None
                    and self.earliest_available_date.tzinfo.utcoffset(
                self.earliest_available_date
            )
                    is not None
            ):
                self.earliest_available_date = self.earliest_available_date.replace(
                    tzinfo=None
                )

            if (
                    self.latest_available_date.tzinfo is not None
                    and self.latest_available_date.tzinfo.utcoffset(
                self.latest_available_date
            )
                    is not None
            ):
                self.latest_available_date = self.latest_available_date.replace(
                    tzinfo=None
                )
        except ValueError as err:
            raise ValueError(
                f"Error validating ticker symbol '{self.instrument}': {err}"
            ) from err

    def _validate_date(self, date_str: str, date_name: str):
        """
        Validates a date string to ensure it is in the correct format and within
        the valid date range for the stock.

        Args:
            date_str (str): The date string to validate.
            date_name (str): A label for the date string (e.g., "Start date" or "End date").
        Raises:
            ValueError: If the date string is not in the 'YYYY-MM-DD' format.
            ValueError: If the date is not within the valid range for the stock's historical data.
        Usage:
            This method is called internally by the _validate_inputs method. It is not intended
            to be called directly.
        """

        if not self.earliest_available_date or not self.latest_available_date:
            raise ValueError(
                "Earliest and latest date info must be available. Validate ticker first."
            )
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if (
                    date_obj.tzinfo is not None
                    and date_obj.tzinfo.utcoffset(date_obj) is not None
            ):
                date_obj = date_obj.replace(tzinfo=None)
        except ValueError as exc:
            raise ValueError(f"{date_name} must be in 'YYYY-MM-DD' format.") from exc

        if date_name == "Start date" and date_obj < self.earliest_available_date:
            raise ValueError(
                f"{date_name} must be on or after the earliest available date for the stock: \
                    {self.earliest_available_date.strftime('%Y-%m-%d')}"
            )

        if date_name == "End date" and date_obj > self.latest_available_date:
            raise ValueError(
                f"{date_name} must be on or before the latest available date for the stock: \
                    {self.latest_available_date.strftime('%Y-%m-%d')}"
            )

    @data_fetch_decorator
    def fetch_raw_data(self) -> Optional[pd.DataFrame]:
        """
        Fetches raw historical price data for self.instrument using
        Yahoo finance.

        Returns:
            Optional[pd.DataFrame]: Raw historical price data for self.instrument.
                                    Returns None if an error occurs of if the data
                                    not available

        Usage:
            >>> AAPL = InstrumentInfo('AAPL', '2020-01-01', '2021-01-01')
            >>> AAPL_RAW_DATA = AAPL.fetch_raw_data()
            >>> print(AAPL_RAW_DATA.head())
        """
        try:
            raw_historical_data = yf.download(
                self.instrument, start=self.start_date, end=self.end_date
            )
            return raw_historical_data
        except ValueError as err:
            raise ValueError(
                f"Error downloading raw historical data for {self.instrument}: {err}"
            ) from err

    def _process_data(self) -> Optional[pd.DataFrame]:
        """
        Processes the raw historical data from _fetch_data.

        The preprocessing steps include:
        - Normalizing column names to lowercase with underscores.
        - Handling missing values via forward-fill.
        - Setting the date as the index if not already set.

        Returns:
            pd.DataFrame: The processed historical data ready for analysis.
        Raises:
            ValueError: If the raw data is empty or processing fails.
        Usage:
            This method is called internally by the _get_historical_data method. It is not intended
            to be called directly.
        """
        raw_historical_data = self.fetch_raw_data()

        if raw_historical_data is None or raw_historical_data.empty:
            raise ValueError("No data available to process.")

        raw_historical_data.columns = [
            col.lower().replace(" ", "_") for col in raw_historical_data.columns
        ]
        raw_historical_data.drop(["volume"], axis=1, inplace=True)

        processed_data = raw_historical_data.ffill()

        if not isinstance(processed_data.index, pd.DatetimeIndex):
            processed_data["date"] = pd.to_datetime(processed_data["date"])
            processed_data = processed_data.set_index("date", inplace=False)

        return processed_data

    def _get_historical_data(self) -> pd.DataFrame:
        """
        Retrieves and processes historical price data for the specified financial instrument.

        This method acts as a wrapper around the _process_data method. It fetches the raw historical
        data using the _fetch_data method and then applies various preprocessing steps defined in
        _process_data. The goal is to provide clean, well-structured, and ready-to-use financial
        data for analysis or strategy development.

        Returns:
            Optional[pd.DataFrame]: A pandas DataFrame containing the processed historical data.
            If data fetching fails or data is unavailable, it returns None.
        Raises:
            ValueError: If any issues occur during data fetching or processing, relevant errors
            will be raised to indicate the failure.
        Usage:
            This method is intended to be called after initializing the InstrumentInfo class with
            valid parameters. It is not meant for direct external use.
        """
        historical_data = self._process_data()

        if historical_data is None or historical_data.empty:
            raise ValueError(f"Could not obtain historical data for {self.instrument}")

        return historical_data

    def generate_line_plot(self) -> None:
        """
        Plots the historical data of the instrument using matplotlib.

        This method generates a line plot for each column in the DataFrame.
        It's useful for visualizing trends in the price data.

        Raises:
            ValueError: If no data is available to plot.
        Usage:
            >>> AAPL = InstrumentInfo('AAPL', '2020-01-01', '2021-01-01')
            >>> AAPL.generate_line_plot()
        """
        if self.historical_data is None or self.historical_data.empty:
            raise ValueError(f"No data for {self.instrument} available to plot")

        self.historical_data.plot(figsize=(10, 6))
        plt.title(f"Historical Data for {self.instrument}")
        plt.xlabel("Date")
        plt.ylabel("Price $")
        plt.legend(title="Metrics")
        plt.grid(True)
        plt.show()
