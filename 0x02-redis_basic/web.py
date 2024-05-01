#!/usr/bin/env python3
"""Implementation of the get page method
"""

import redis
from functools import wraps
import requests

re = redis.Redis()


def url_access_count(method):
    """method for decorating the get-page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper method"""
        key - "cached:" + url
        cached_value = re.get(key)
        if cached_value:
            return cached_value.decode('utf-8')

        key_count = "count:" + url
        html_content = method(url)

        re.incr(key_count)
        re.set(key, html_content, ex=10)
        re.expire(key, 10)
        return html_content
    return wrapper

    @url_access_count
    def get_page(url: str) -> str:
        """method to get page"""
        results = requests.get(url)
        return results.text

    if __name__ == "__main__":
        get_page('http://slowwly.robertomurray.co.uk')
