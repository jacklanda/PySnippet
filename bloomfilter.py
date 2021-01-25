#! /bin/python3
# coding: utf-8
# Author: Jacklanda

import mmh3
import redis


class BloomFilter(object):
    """
    An Implementation of BloomFilter based on Redis

    Usage:

    ```python
    >>> from bloomfilter import BloomFilter
    >>> bf = BloomFilter()
    >>> bf.add("something")
    >>> bf.is_exist("something")
    True
    ```

    Params:
    - host: the Redis host, default="localhost"
    - port: the Redis port, default=6379
    - db: the Redis database, default=0
    - key: the key corresponde to BloomFilter Instance, default="BloomFilter"
    - bit_size: specify the bit size of bit array in redis, default=10,000,000
    """

    def __init__(self,
                 host="localhost",
                 port=6379,
                 db=0,
                 key='BloomFilter',
                 bit_size=10000000):
        self.r_client = redis.Redis(host=host, port=port, db=db)
        self.key = key
        self.bit_size = bit_size
        # initiate a list contained 9 hash seeds
        self.seeds = [11, 22, 33, 44, 55, 66, 77, 88, 99]

    def __contains__(self, val):
        """
        implementation for "in" syntax 
        to traverse some seq like list, set, tuple, etc

        Usage:

        ```python
        >>> from bloomfilter import BloomFilter
        >>> bf = BloomFilter()
        >>> "hello kitty" in bf
        False
        >>> bf.add("hello kitty")
        >>> "hello kitty" in bf
        True
        ```

        Params:
        - val: the input key to be judged
        """
        return self.is_exist(val)

    def _calc_offsets(self, content):
        return [mmh3.hash(content, seed) % self.bit_size for seed in self.seeds]

    def is_exist(self, content: str) -> bool:
        if not content:
            return False
        locs = self._calc_offsets(content)

        return all(True if self.r_client.getbit(self.key, loc) else False for loc in locs)

    def add(self, val):
        if(isinstance(val, str)):
            locs = self._calc_offsets(val)
            for loc in locs:
                self.r_client.setbit(self.key, loc, 1)
        elif(isinstance(val, list)
                or isinstance(val, set)
                or isinstance(val, tuple)):
            for item in val:
                locs = self._calc_offsets(item)
                for loc in locs:
                    self.r_client.setbit(self.key, loc, 1)
        else:
            raise TypeError(
                "INPUT ERROR -> INPUT TYPE COULD ONLY BE: Str, List, Set, Tuple OBJECT!")


if __name__ == '__main__':
    bf = BloomFilter()

    test_str = 'https://google.com'

    print('Before-adding: ', end="")
    if bf.is_exist(test_str):
        print(test_str + ' is existed')
    else:
        print(test_str + ' is not existed')

    bf.add(test_str)

    print('After-adding: ', end="")
    if bf.is_exist(test_str):
        print(test_str + ' is existed')
    else:
        print(test_str + ' is not existed')
