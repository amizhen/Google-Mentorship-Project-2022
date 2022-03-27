import functools
import re
from typing import Any, Callable, Mapping, Sequence, Union


class Filter:
    """
    A class that will filter a sequence of mapping of data as specified by the user.

    Examples on how to use the decorator:

        Example 1: Pass in a function

            def less_than_ten(data : Mapping[str, Any]) -> bool:
                return data["test"] < 10

            @Filter(less_than_than)
            def getData() -> Sequence[Mapping[str, Any]]:
                return INSERT_SEQUENCE_OF_DATA

            This method is better for more complex filters

        Example 2: Use anonymous functions / lambdas

            @Filter(lambda data : data["test] < 10)
            def getData() -> Sequence[Mapping[str, Any]]:
                return INSERT_SEQUENCE_OF_DATA

            This method is better for simpler filters

        Example 3: Non-decorator method

            def getData() -> Sequence[Mapping[str, Any]]:
                return INSERT_SEQUENCE_OF_DATA

            less_than_ten = Filter(lambda data : data["test"] < 10)(getData)
            greater_than_ten = Filter(lambda data : data["test"] > 10)(getData)

            This method is better if you want to reuse the same function that is being wrapped
            in other filters.

    While you can have multiple filter decorators on a single function, this should be avoided. 
    Instead, you should combine the two filters into a single filter function to pass into the
    decorator.

    The filter function should also be careful in type checking as TypeErrors may be thrown
    if you do not cast the value correctly.

    The class comes with some predefined filters that may be used.
    """

    def __init__(self, filter_func: Callable[[Mapping[str, Any]], bool]):
        """
        Initializes the filter decorator

        Args:
            filter_func: 
                The filter function accepts a mapping of data and returns a boolean.
                It will be used to filter a sequence of mapping of data
        """

        self._filter_func = filter_func

    def __call__(self, func: Callable[[], Sequence[Mapping[str, Any]]]) -> Callable[[], Sequence[Mapping[str, Any]]]:
        """
        Returns a wrapper function to be used as a filter decorator

        Args:
            func: A function that returns a sequence of mapping of data to be filtered

        Returns:
            A sequence of mapping after the filter has been applied
        """

        @functools.wraps(func)
        def wrapper():
            filtered = []
            data = func()
            for datum in data:
                if self._filter_func(datum):
                    filtered.append(datum)
            return filtered
        return wrapper

    @staticmethod
    def get_value(path: str, data: Mapping[str, Any]) -> Union[Any, None]:
        """
        Fetches the value in data mapping from the path of its location.

        Path needs to be keys within the data mapping. To access nested mappings, use `/`, `\`, or `.`.
        For example, a Mapping["key1"]["key2"] path would be `key1/key2`

        Args:
            path: 
                A valid path string to the location of the data you want to retrieve in the data mapping
            data:
                A mapping of a string key to any type value. Contains the value you want to retrieve

        Returns: 
            The value found in the data mapping from the provided path

        Raises:
            ValueError: The path cannot be empty 
            KeyError: The path is incorrectly formatted
        """

        if not path:
            raise ValueError("The path can not be empty")
        paths = re.split(r"[.\/\\]", path)
        get = data.get(paths[0])
        for p in paths[1:]:
            get = get.get(p)
        return get

    @classmethod
    def less_than(cls, path: str, value: Any) -> "Filter":
        """
        A class method that returns a custom less than Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be less than in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) < value
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def greater_than(cls, path: str, value: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom greater than Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be greater than in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) > value
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def less_than_equal_to(cls, path: str, value: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom less than or equal to Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be less than or equal to in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) <= value
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def greater_than_equal_to(cls, path: str, value: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom greater than or equal to Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be greater than or equal to in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) >= value
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def in_range_inclusive(cls, path: str, lower_bound: Union[float, int, str], upper_bound: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom in range inclusive Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            lower_bound:
                A value that is the lower bound of the range
            upper_bound:
                A value that is the upper bound of the range

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) >= lower_bound and Filter.get_value(path, data) <= upper_bound
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def in_range_exclusive(cls, path: str, lower_bound: Union[float, int, str], upper_bound: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom in range exclusive Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            lower_bound:
                A value that is the lower bound of the range
            upper_bound:
                A value that is the upper bound of the range

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) > lower_bound and Filter.get_value(path, data) < upper_bound
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def equal_to(cls, path: str, value: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom equal to Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be equal to in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) == value
            except TypeError:
                return False
        return cls(wrapping)

    @classmethod
    def not_equal_to(cls, path: str, value: Union[float, int, str]) -> "Filter":
        """
        A class method that returns a custom not equal to Filter decorator

        Args:
            path: 
                The path to the data in the data mapping
            value:
                A value that the data should be not equal to in the filter

        Returns:
            The filter object that will be used as a decorator
        """

        def wrapping(data: Mapping[str, str]) -> bool:
            try:
                return Filter.get_value(path, data) and Filter.get_value(path, data) != value
            except TypeError:
                return False
        return cls(wrapping)