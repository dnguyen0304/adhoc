# -*- coding: utf-8 -*-

import abc


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
