"""A debug module using logging.

@author: Christophe
@email: sdl.office.1997@gmail.com
"""
import traceback
import logging
from functools import wraps


class Tracker:
    """A logging context manager.

    Usage:
        with Tracker() as tracker:
            tracker.info("it's a example")
    then you got the output:
    2017-10-31 22:44:39,612 - root: INFO
    it's a example
    """

    _fmt = '%(asctime)s - %(name)s: %(levelname)s\n%(message)s'

    def __init__(self, name=None, path=None, level=logging.DEBUG, fmt=None):
        if fmt is None:
            fmt = self._fmt
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if path is not None:
            if not isinstance(path, list):
                path = [path]
            for filename in path:
                file_handle = logging.FileHandler(filename)
                file_handle.setLevel(level)
                file_handle.setFormatter(logging.Formatter(self._fmt))
                self.logger.addHandler(file_handle)
        self.stream_handle = logging.StreamHandler()
        self.stream_handle.setLevel(level)
        self.stream_handle.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(self.stream_handle)

    def __enter__(self):
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handle in self.logger.handlers:
            self.logger.removeHandler(handle)
            handle.close()


def hook(path=None, level=logging.DEBUG, fmt=None):
    """A logging decorator track the func.

    :param path: the path of log file, use list if more than path.
    :param level: the logging level, default is logging.DEBUG
    :param fmt: the logging fmt, default use '%(asctime)s - %(name)s: %(levelname)s\n%(message)s'
    """
    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func.__name__
            arg_str = ', '.join(repr(arg) for arg in args)
            kwarg_str = ', '.join('{}={}'.format(repr(key),
                                                 kwargs[key]) for key in kwargs.keys())
            func_str = "func {}({})".format(name, arg_str + kwarg_str)

            with Tracker(name, path=path, level=level, fmt=fmt) as tracker:
                tracker.debug(' '.join((func_str, "start.")))
                try:
                    result = func(*args, **kwargs)
                    tracker.debug(' '.join((func_str, "finished.")))
                    result_str = ' '.join((func_str, "result -> {}.".format(result)))
                    tracker.info(result_str)
                    return result
                except Exception as inst:
                    tracker.warning(repr(inst))
                    tracker.debug(traceback.format_exc())
                    tracker.info(' '.join((func_str, "exit 1.")))

        return wrapper

    return decorate
