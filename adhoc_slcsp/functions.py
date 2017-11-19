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


class MergeZipCodes(Pipeline):

    def __init__(self, reader):

        """
        Merge with the ZIP code lookup.

        Parameters
        ----------
        reader : adhoc_slcsp.io.Reader
        """

        self._reader = reader

    def __call__(self, df):
        # This could be read into memory once and passed as a singleton
        # dependency.
        zip_codes = self._reader.read()
        # Filter ZIP codes associated with multiple rate areas. The
        # rates for these ZIP codes are ambiguous.
        # This could be processed and persisted to avoid running the
        # computation every time.
        zip_codes = zip_codes.loc[:, ['zipcode', 'state', 'rate_area']] \
                             .groupby('zipcode') \
                             .filter(lambda x: len(x.drop_duplicates()) == 1) \
                             .drop_duplicates()
        # This raises an uncaught KeyError if the label cannot be
        # found in both data frames.
        merged = df.merge(zip_codes, how='left', on='zipcode')
        return merged

    def __repr__(self):
        repr_ = '{}(reader={})'
        return repr_.format(self.__class__.__name__, self._reader)
