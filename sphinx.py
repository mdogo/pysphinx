from sphinxapi import *


class SphinxQuery():
    def __init__ (self):
        pass


class SphinxIndex():
    _name = '' # The name of the index.

    _delta = None # The delta index for this index. By default None
    """
    A note here.
    A delta index can have also another delta index. The structure may be
    something like this.

    Main Index -> First Delta Index -> Second Delta Index ...
    """

    def __init__ (self):
        pass


class SphinxServer():
    _host = 'localhost' # The host of the server. By default localhost.
    _port = 9312 # The port of the server. By default 9312.

    _indices = [] # A list of indices stored in this server.
    _queries = [] # A list of batch queries to be executed.


    def __init__ (self):
        pass

    
    def _get_client(self):
        client = SphinxClient()
        if self._host != 'localhost' or self._port != 9312:
            client.SetServer(host=self._host, port=self._port)
        return client


    def add_query(self, query):
        _queries.append(query)


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
