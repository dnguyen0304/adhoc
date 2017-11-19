# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from .. import functions
from .. import io


class TestMergeZipCodes:

    def __init__(self):
        self.columns = None
        self.df = None
        self.merge_zip_codes = None
        self.expected = None

    def setup(self):
        self.columns = ('zipcode', 'state', 'rate_area')
        data = ['00000', '00001']
        self.df = pd.Series(data=data, name=self.columns[0]).to_frame()

    def test_call(self):
        input_data = [('00000', 'FO', 0),
                      ('00001', 'OB', 1),
                      ('00002', 'AR', 2)]
        expected_data = [('00000', 'FO', 0),
                         ('00001', 'OB', 1)]
        self._set_up(input_data=input_data, expected_data=expected_data)

        merged = self.merge_zip_codes(df=self.df)
        pd.testing.assert_frame_equal(self.expected, merged)

    def test_call_filters_ambiguous_zip_codes(self):
        input_data = [('00000', 'FO', 0),
                      ('00001', 'OB', 1),
                      ('00001', 'OB', 2),
                      ('00002', 'AR', 2)]
        expected_data = [('00000', 'FO', 0),
                         ('00001', np.NaN, np.NaN)]
        self._set_up(input_data=input_data, expected_data=expected_data)

        merged = self.merge_zip_codes(df=self.df)
        pd.testing.assert_frame_equal(self.expected, merged)

    def _set_up(self, input_data, expected_data):
        zip_codes = pd.DataFrame.from_records(data=input_data,
                                              columns=self.columns)
        reader = io.MockReader(df=zip_codes)
        self.merge_zip_codes = functions.MergeZipCodes(reader=reader)
        self.expected = pd.DataFrame.from_records(data=expected_data,
                                                  columns=self.columns)
