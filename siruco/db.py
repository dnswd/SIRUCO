import psycopg2
from os import getenv
from urllib.parse import urlparse

# Adapted from https://gist.github.com/goldsborough/8928226434b38f7102b3


class Database:
    '''
    A wrapper around the psycopg2 python library.

    The Database class is a high-level wrapper around the psycopg2
    library. It allows users to create a postgresql database connection and
    write to or fetch data from the selected database.
    '''

    def __init__(self, url=getenv("DATABASE_URL", None)):
        self.conn = None
        self.cursor = None

        if url:
            self.open(url)

    def open(self, url):
        '''
        Opens a new database connection.

        @param url The url of the database to open.

        This function manually opens a new database connection. The database
        can also be opened in the constructor or as a context manager.
        '''
        
        self.url = urlparse(url)
        self.conn = psycopg2.connect(database=self.url.path[1:],
                                     user=self.url.username,
                                     password=self.url.password,
                                     host=self.url.hostname,
                                     port=self.url.port
                                     )
        self.cursor = self.conn.cursor()

    def close(self):
        '''
        Function to close a database connection.

        The database connection needs to be closed before you exit a program,
        otherwise changes might be lost. You can also manage the database
        connection as a context manager, then the closing is done for you. If
        you opened the database connection with the open() method or with the
        constructor ( \\__init\\__() ), you must close the connection with this
        method.

        @see open()

        @see \\__init\\__()
        '''

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def query(self, query, limit=None):
        self.cursor.execute(query)

        # fetch data
        if "insert" in query.lower():
            rows = self.cursor.fetchall()
            return rows[len(rows)-limit if limit else 0:]

        return self.cursor.rowcount

    def summary(self, rows):
        # split the rows into columns
        cols = [[r[c] for r in rows] for c in range(len(rows[0]))]

        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        def time(col): return "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        summary_ = {}

        for c in cols:
            summary_["hi"] = max(c)
            summary_["hi_t"] = time(c.index(max(c)))

            summary_["lo"] = min(c)
            summary_["lo_t"] = time(c.index(min(c)))

            summary_["avg"] = sum(c)/len(rows)

        return summary_
