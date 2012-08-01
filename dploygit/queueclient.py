import zmq


class BuildQueueClient(object):
    """Client to the dploy-center build queue"""
    def __init__(self, uri, context=None):
        self._uri = uri
        self._context = context
        self._current_socket = None

    def _connect_to_socket(self):
        """Lazily connect to the socket"""
        context = self._context
        if not context:
            context = zmq.Context()
            self._context = context
        socket = context.socket(zmq.REQ)
        socket.connect(self._uri)
        return socket

    def _close_socket(self):
        socket = self._current_socket
        socket.close()
        self._current_socket = None

    @property
    def current_socket(self):
        current_socket = self._current_socket
        if not current_socket:
            self._current_socket = self._connect_to_socket()
            current_socket = self._current_socket
        return current_socket

    def send_deploy_request(self, deploy_request):
        socket = self.current_socket
        # Send request
        socket.send_json(deploy_request.to_dict())
        # Wait for response
        response = socket.recv_json()
        return response
