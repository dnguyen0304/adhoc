# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from nose.tools import assert_in

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


class TestMergePlans:

    def __init__(self):
        self.columns = None
        self.df = None
        self.merge_plans = None
        self.expected = None

    def setup(self):
        self.columns = ('state', 'rate_area', 'rate')
        data = [('FO', 0),
                ('OB', 1),
                ('AR', 2)]
        self.df = pd.DataFrame.from_records(data=data,
                                            columns=self.columns[:2])

    def test_call(self):
        input_data = expected_data = [('FO', 0, 0.0),
                                      ('OB', 1, 1.0),
                                      ('AR', 2, 2.0)]
        self._set_up(input_data=input_data, expected_data=expected_data)

        merged = self.merge_plans(df=self.df)
        pd.testing.assert_frame_equal(self.expected, merged)

    def test_call_applies_left_join(self):
        input_data = [('FO', 0, 0.0),
                      ('OB', 1, 1.0)]
        expected_data = [('FO', 0, 0.0),
                         ('OB', 1, 1.0),
                         ('AR', 2, np.NaN)]
        self._set_up(input_data=input_data, expected_data=expected_data)

        merged = self.merge_plans(df=self.df)
        pd.testing.assert_frame_equal(self.expected, merged)

    def test_call_has_rates_column(self):
        input_data = [('FO', 0, 0.0),
                      ('OB', 1, 1.0),
                      ('AR', 2, 2.0)]
        self._set_up(input_data=input_data, expected_data=list())

        # Set up a column label conflict.
        data = [('FO', 0, None),
                ('OB', 1, None),
                ('AR', 2, None)]
        self.df = pd.DataFrame.from_records(data=data, columns=self.columns)

        merged = self.merge_plans(df=self.df)
        assert_in('rates', merged)

    def _set_up(self, input_data, expected_data):
        plans = pd.DataFrame.from_records(data=input_data,
                                          columns=self.columns)
        reader = io.MockReader(df=plans)
        self.merge_plans = functions.MergePlans(reader=reader)
        self.expected = pd.DataFrame.from_records(data=expected_data,
                                                  columns=self.columns)
