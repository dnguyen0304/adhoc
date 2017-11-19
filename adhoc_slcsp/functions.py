# -*- coding: utf-8 -*-

import abc


# Python does not support a feature to define function interfaces
# similar to the abc library for class interfaces.
class Pipeline(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __call__(self, df):

        """
        Apply arbitrary computations.

        The input may be mutated in-place.

        Parameters
        ----------
        df : pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
        """

        raise NotImplementedError
