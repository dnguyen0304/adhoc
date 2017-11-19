# -*- coding: utf-8 -*-


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
