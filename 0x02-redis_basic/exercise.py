#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.
"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """counts how many times cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """a function that wraps decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Method for storing the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """method that wraps call history decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":ouptuts", output)
        return output

    return wrapper


def replay(fn: Callable):
    """method to display history of calls"""
    rep = redis.Redis()
    function_name = fn.__qualname__
    value = rep.get(function_name)
    try:
        value = int(value.decode('utf-8'))
    except Exception:
        value - 0

    print(f"{function_name} was called {value} times")
    input = rep.lrange(f"{function_name}:inputs", 0, -1)
    output = rep.lrange(f"{function_name}:outputs", 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode('utf-8')
        except Exception:
            input = ""

        try:
            output = output.decode('utf-8')
        except Exception:
            output = ""

        print(f"{function_name}(*{input}) -> {output}")


class Cache:
    """Creating a Cache Class"""

    def __init__(self):
        """Dunder function to store the instance of Redis Client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Function that generates a random key"""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """Function that convert data back to required format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Function automatically parameterize cache.get"""
        value - self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """function aht parameterize cache.get to integer"""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
