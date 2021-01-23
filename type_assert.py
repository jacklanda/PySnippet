#! /bin/python3
# Excerpted From: Python Cookbook Chapter9: 9-7

from inspect import signature
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    """
    An simple decorator for Python basic datatype detection,
    support like int, float, string, list, set, tuple, dic, etc.

    Usage:

    ```python
    >>> from type_assert import typeassert
    >>> @typeassert(int, int)
    >>> def add(x, y):
    ...     return x + y
    ```

    Parameters:
    ty_args
    ty_kwargs
    """
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(
                                name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate
