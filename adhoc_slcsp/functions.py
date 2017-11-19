# -*- coding: utf-8 -*-

import abc

import numpy as np


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


class MergePlans(Pipeline):

    def __init__(self, reader):

        """
        Merge with the plan lookup.

        Parameters
        ----------
        reader : adhoc_slcsp.io.Reader
        """

        self._reader = reader

    def __call__(self, df):
        # This could be read into memory once and passed as a singleton
        # dependency.
        plans = self._reader.read()
        # This raises an uncaught KeyError if the labels cannot be
        # found in both data frames.
        merged = df.merge(plans, how='left', on=['state', 'rate_area'])
        # Fix the column label.
        merged.rename(columns={
                          'rate_y': 'rates'
                      },
                      inplace=True)
        return merged

    def __repr__(self):
        repr_ = '{}(reader={})'
        return repr_.format(self.__class__.__name__, self._reader)


class CalculateSlcsp(Pipeline):

    def __call__(self, df):

        """
        Calculate the second lowest cost silver plan (slcsp).
        """

        slcsp = df.loc[:, ['zipcode', 'rates']] \
                  .groupby('zipcode') \
                  .apply(self._helper)
        # An alternative is to use pandas.Series.rename.
        slcsp.name = 'rate'
        # Update the index to maintain the original order.
        # Remove the duplicated rows created by the merge (one-to-many
        # SQL LEFT JOIN).
        processed = slcsp.reindex(df.loc[:, 'zipcode'].drop_duplicates())
        processed = processed.to_frame()
        return processed

    @staticmethod
    def _helper(group):

        """
        Parameters
        ----------
        group : pandas.DataFrame

        Returns
        -------
        float
        """

        try:
            # This is equivalent to a vectorized sorted(rates)[-2],
            # which has a time complexity of O(n log n) where n is the
            # number of elements in the iterable.
            slcsp = group.loc[:, 'rates'].nsmallest(2).values[1]
        except IndexError:
            slcsp = np.NaN
        return slcsp

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
