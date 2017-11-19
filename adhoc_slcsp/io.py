# -*- coding: utf-8 -*-

import abc

import pandas as pd


class Reader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self):

        """
        Read the source into a data frame.

        Returns
        -------
        pandas.DataFrame
        """

        raise NotImplementedError


class Writer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def write(self, df):

        """
        Write the data frame into a destination.

        Parameters
        ----------
        df : pandas.DataFrame
        """

        raise NotImplementedError


class CsvReader(Reader):

    def __init__(self, path):

        """
        Read from a CSV source.

        Parameters
        ----------
        path : str
        """

        self._path = path

    def read(self):
        return pd.read_csv(self._path)

    def __repr__(self):
        repr_ = '{}(path="{}")'
        return repr_.format(self.__class__.__name__, self._path)


class CsvWriter(Writer):

    def __init__(self, path):

        """
        Write to a CSV destination.

        Parameters
        ----------
        path : str
        """

        self._path = path

    def write(self, df):
        df.to_csv(self._path)

    def __repr__(self):
        repr_ = '{}(path="{}")'
        return repr_.format(self.__class__.__name__, self._path)
