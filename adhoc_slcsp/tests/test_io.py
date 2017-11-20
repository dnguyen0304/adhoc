# -*- coding: utf-8 -*-

import pandas as pd

from .. import io


def test_prepending_reader():

    # setup
    expected = pd.Series(data=['00001', '12345'])
    df = pd.DataFrame.from_dict(data={'zipcode': [1, 12345]})
    reader = io.PrependingReader(reader=io.MockReader(df=df))

    # test
    output = reader.read()
    pd.testing.assert_series_equal(expected,
                                   output.loc[:, 'zipcode'],
                                   check_names=False)
