from sphinxapi import *


class SphinxQuery():
    pass


class SphinxIndex():
    name = ''


class SphinxServer():
    host = 'localhost'
    port = 9312
    def status(self):
        """
        Return the status of the Sphinx server.
    
        TODO: Document error and warning responses.
        """
        client = SphinxClient()
        if host != 'localhost' or port != 9312:
            client.SetServer(host=self.host, port=self.port)
        # We make a very small query against the index to see if eveything is
        # working fine. If a error or warning is retrieved we return that
        # error or warning. In other case we return a message saying the
        # Sphinx server has no problems.
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
        return ''
