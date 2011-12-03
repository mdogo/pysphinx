from sphinxapi import *


class SphinxQuery():
    def __init__ (self):
        self._offset = 0
        self._limit = 10
        self._maxmatches = 1000
        self._cutoff = 0

        self._maxquerytime = 0


    def set_limits(self, offset, limit, maxmatches=0, cutoff=0):
        if not(type(offset) in [int,long] and 0<=offset):
            raise TypeError('offset must be unsigned int or long')
        if not(type(limit) in [int,long] and 0<=limit):
            raise TypeError('limit must be unsigned int or long')
        if not(type(maxmatches) in [int,long] and 0<=maxmatches):
            raise TypeError('maxmatches must be unsigned int or long')
        if not(type(cutoff) in [int,long] and 0<=cutoff):
            raise TypeError('cutoff must be unsigned int or long')
        self._offset = offset
        self._limit = limit
        self._maxmatches = maxmatches
        self._cutoff = cutoff


    def set_max_query_time(self, maxquerytime):
        if not(type(maxquerytime) in [int] and 0<=offset):
            raise TypeError('maxquerytime must be unsigned int')
        self._maxquerytime = maxquerytime
    

class SphinxIndex():
    def __init__ (self):
        self._name = '' # The name of the index.

        self._delta = None # The delta index for this index (default None)
        """
        A note here.
        A delta index can have also another delta index. The structure may be
        something like this.

        Main Index -> First Delta Index -> Second Delta Index ...
        """


class SphinxServer():
    def __init__ (self):
        self._host = 'localhost' # The host of the server (default is localhost)
        self._port = 9312 # The port of the server (default is 9312)

        self._indices = [] # A list of indices stored in this server.
        self._queries = {} # A index of matchmode and list of batch queries
                           # to be executed.

    
    def _get_client(self):
        client = SphinxClient()
        if self._host != 'localhost' or self._port != 9312:
            client.SetServer(host=self._host, port=self._port)
        return client


    def add_query(self, query):
        if not isinstance(query, SphinxQuery):
            raise TypeError('query must be SphinxQuery')
        if self._queries.has_key(query._mode):
            self._queries[query._mode].append(query)
        else:
            self._queries[query._mode] = [query]


    def run_queries(self):
        result = []
        client = self._get_client()
        for matchmode, query in self._queries.iteritems():
            # Apply filters, order by and eveything else
            result.append(client.RunQueries())
            error = client.GetLastError()
            if error:
                return error
        return result


    def status(self):
        """
        Return an error if there is some problem in the server or indices.
        In other case it returns the status of the Shphinx server.
    
        TODO: Document error and warning responses.
        """
       
        client = self._get_client()
        # We make a very small query against the index to see if eveything is
        # working fine. If a error or warning is retrieved we return that
        # error or warning. In other case we return the status of the server.
        client.SetLimits(offset=0,
                         limit=1,
                         maxmatches=1,
                         cutoff=1)
        client.Query('')
        error = client.GetLastError()
        if error:
            return error
        warning = client.GetLastWarning()
        if warning:
            return warning
        return client.Status()
