import json
import os
import time
from functools import wraps


def file_cache(filename):
    def decorator(func):
        @wraps(func)
        def cached_function(*args, **kwargs):
            cache = read(filename)
            if cache:
                print "using cache"
                return cache
            else:
                result = func(*args, **kwargs)
                common.save(result, filename)
            return result
        return cached_function
    return decorator


def touch(filename, times=None):
    print "filename: ", filename
    with open(filename, 'a'):
        os.utime(filename, times)


def save(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True,
                           indent=4,
                           separators=(',', ': '))


def read(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (IOError, ValueError):
        return None
