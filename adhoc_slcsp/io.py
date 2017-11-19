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
