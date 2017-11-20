# -*- coding: utf-8 -*-

import logging

from adhoc_slcsp import functions
from adhoc_slcsp import io


class Application:

    def __init__(self, reader, funcs, writer):

        """
        Parameters
        ----------
        reader : adhoc_slcsp.io.Reader
        funcs : typing.Iterable[adhoc_slcsp.functions.Pipeline]
        writer : adhoc_slcsp.io.Writer
        """

        self._reader = reader
        self._funcs = funcs
        self._writer = writer

    def start(self):

        """
        Start the application.
        """

        df = self._reader.read()
        for func in self._funcs:
            df = df.pipe(func=func)
        self._writer.write(df=df)

    def __repr__(self):
        repr_ = '{}(reader={}, funcs={}, writer={})'
        return repr_.format(self.__class__.__name__,
                            self._reader,
                            self._funcs,
                            self._writer)


def main():

    # Set the configuration.
    source_path = './data/slcsp.csv'
    zip_codes_path = './data/zips.csv'
    plans_path = './data/plans.csv'
    processed_path = './data/slcsp-processed.csv'

    # Create the reader.
    reader = io.CsvReader(path=source_path)

    # Include prepending.
    reader = io.PrependingReader(reader=reader)

    # Create the functions.
    funcs = [
        functions.MergeZipCodes(
            reader=io.PrependingReader(reader=io.CsvReader(path=zip_codes_path))),
        functions.MergePlans(reader=io.CsvReader(path=plans_path)),
        functions.CalculateSlcsp()]

    # Create the logger.
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.formatter = simple_formatter
    logger = logging.getLogger(name=__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    # Include logging.
    funcs = (functions.Logging(func=func, logger=logger) for func in funcs)

    # Create the writer.
    writer = io.CsvWriter(path=processed_path)

    # Create the application.
    application = Application(reader=reader, funcs=funcs, writer=writer)

    application.start()


if __name__ == '__main__':
    main()
