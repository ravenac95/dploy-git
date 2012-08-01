import zmq


class BroadcastListener(object):
    def __init__(self, uri, output, context=None):
        self._uri = uri
        self._output = output
        self._context = context
        self._current_socket = None

    def _connect_to_socket(self):
        print "hello"
        context = self._context
        if not context:
            context = zmq.Context()
            self._context = context
        socket = context.socket(zmq.SUB)
        socket.connect(self._uri)
        return socket

    @property
    def current_socket(self):
        current_socket = self._current_socket
        if not current_socket:
            self._current_socket = self._connect_to_socket()
            current_socket = self._current_socket
        return current_socket

    def _close_socket(self):
        socket = self._current_socket
        socket.close()
        self._current_socket = None

    def prepare(self):
        # Connect
        self.current_socket

    def listen_from_response(self, response):
        socket = self.current_socket
        socket.setsockopt(zmq.SUBSCRIBE, str(response['id']))

        self._output.line("Listening to build on channel %s" % response['id'])

        while True:
            message = socket.recv_multipart()
            id, output = message
            if output.strip() == '---END---':
                break
            self._output.write(output)
