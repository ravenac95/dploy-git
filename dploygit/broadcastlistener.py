class BroadcastListener(object):
    def __init__(self, uri, output):
        self._uri = uri
        self._output = output

    def listen_from_response(self, response):
        self._output.line(response)
        self._output.line('Hello there world!')
