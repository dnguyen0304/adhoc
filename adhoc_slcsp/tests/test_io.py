# -*- coding: utf-8 -*-

import pandas as pd

from .. import io


class MockReader(io.Reader):

    def __init__(self, df):

        """
        Read from a data frame source.

        Parameters
        ----------
        df : pandas.DataFrame
        """

        self._df = df

    def read(self):
        return self._df

    def __repr__(self):
        repr_ = '{}(df={})'
        return repr_.format(self.__class__.__name__, self._df)


def test_prepending_reader():

    # setup
    expected = pd.Series(data=['00001', '12345'])
    df = pd.DataFrame.from_dict(data={'zipcode': [1, 12345]})
    reader = io.PrependingReader(reader=MockReader(df=df))

    # test
    output = reader.read()
    pd.testing.assert_series_equal(expected,
                                   output.loc[:, 'zipcode'],
                                   check_names=False)
