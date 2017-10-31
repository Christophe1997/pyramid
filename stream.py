"""Files generator for batch operator.

@author: Christophe
@email: sdl.1997.office@gmail.com
"""
import os
import pandas as pd
from sklearn.externals import joblib
from functools import partial


class Stream:
    """File stream class.

    Operate the file_dir like generator.
    Usage:
        csv_stream = Stream(csv_dir, typecode='data')
        for csv in csv_stream:
            print(isinstalce(csv, pd.DataFrame)) # True
    """
    data_mode = {
        'data': partial(pd.read_csv, encoding="utf-8"),
        'skl_model': joblib.load
    }

    def __init__(self, file_dir, typecode=None, ignore_files=None, batchsize=1):
        if isinstance(file_dir, list) or isinstance(file_dir, tuple):
            self._list = list(file_dir)
        else:
            self._list = [os.path.join(file_dir, x) for x in os.listdir(file_dir)]
        self.typecode = typecode
        self._batchsize = batchsize
        self._ignore_files = ignore_files
        self._list = list(set(self._list).difference(self._ignore_files))
        self._now = None
        self._tag = 0
        if self.typecode not in self.data_mode.keys():
            raise KeyError(self.typecode)
        self._process = self.data_mode.get(self.typecode, lambda stream: stream.now)

    def __iter__(self):
        return self

    def __next__(self):
        self._tag = self._tag + self._batchsize
        self._now = self._list[self._tag - self._batchsize: self._tag]
        if not self.now:
            raise StopIteration
        if len(self.now) == 1:
            return self._process(self.now[0])
        else:
            return [self._process(filename) for filename in self.now]

    @property
    def now(self):
        if self._batchsize == 1:
            return self._now[0]
        return self._now
