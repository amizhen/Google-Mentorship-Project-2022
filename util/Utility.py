import time
from typing import Callable

def time_it(func) -> Callable[[], int]:
    """
    A decorator to time functions

    Args:
        func: The func to time

    Returns:
        The wrapper function that returns the time it took for the function to execute
    """

    def wrapper(*args, **kwargs) -> int:
        start = time.time()
        func(*args, **kwargs)
        return time.time() - start
    return wrapper