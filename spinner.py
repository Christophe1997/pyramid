"""A decorator for rotating spin waiting func run over.

@author: Christophe
@email: sdl.office.1997@gmail.com
"""
import threading
from itertools import cycle
from functools import wraps
import time
import sys


class Signal:
    go = True


def spin(msg, signal):
    """A spin, the code is same as which writen in Fluent Python

    :param msg: message while waiting
    :param signal: Signal object control the spin
    :return:
    """
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in cycle('\/-\\'):
        status = ''.join((char, ' ', msg))
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
        write(' ' * len(status) + '\x08' * len(status))


def spinner(msg):
    """The main decorator.

    :param msg: message while waiting
    """

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            arg_str = ', '.join(repr(arg) for arg in args)
            kwarg_str = ', '.join('{}={}'.format(repr(key),
                                                 kwargs[key]) for key in kwargs.keys())

            signal = Signal()
            _spinner = threading.Thread(target=spin, args=(msg, signal))
            start = time.perf_counter()
            _spinner.start()
            result = func(*args, **kwargs)
            elapsted = time.perf_counter() - start
            signal.go = False
            _spinner.join()

            print('func {}({}) takes {:.8f}s'.format(name, arg_str + kwarg_str, elapsted))
            return result

        return wrapper

    return decorate
