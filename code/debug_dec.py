"""
Decorator to help in debugging functions

  Created by Ed on 4/17/2019
 """
import functools


def debug(function):
    @functools.wraps(function)
    def _debug(*args, **kwargs):
        output = function(*args, **kwargs)
        print(f'{function.__name__},({args}, {kwargs}): {output}')
        return output
    return _debug

def spam(eggs):
    return 'spam' * (eggs % 5)

if __name__ == '__main__':

    output = spam(3)

