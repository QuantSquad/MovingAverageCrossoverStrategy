"""
This module contains the definition for the data_fetch_decorator
which is used to wrap the src.data_collection.InstrumentInfo.fetch_raw_data()
method.
"""

from typing import Callable, TypeVar
import functools
import requests

# Type variable used for the return type of the inner function.
R = TypeVar('R')


def data_fetch_decorator(func: Callable[..., R]) -> Callable[..., R]:
    """
    A decorator that prints informative messages before and after the
    execution of a data-fetching function.

    It assumes the first argument of the decorated function is an object
    with 'instrument', 'start_date', and 'end_date' attributes, typically
    an instance of a data-fetching class.

    Args:
        - func (Callable[..., R]): The function to be decorated.
    Returns:
        - Callable[..., R]: A wrapped version of the function with additional
          logging before and after its execution.
    Raises:
        - ConnectionError: If an HTTPError occurs during the function execution.
    Usage:
        >>> @data_fetch_decorator
            def _fetch_raw_data():
                pass
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> R:
        print("-" * 70)
        print(f"Fetching data for {args[0].instrument} from \
        {args[0].start_date} to {args[0].end_date}...")
        try:
            result = func(*args, **kwargs)
            print("Data fetched successfully.")
            print("-" * 70)
            return result
        except requests.exceptions.HTTPError as err:
            raise ConnectionError(
                f"HTTP error occurred while fetching data: {err}") from err

    return wrapper
