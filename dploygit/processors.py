class PreReceiveProcessor(object):
    def __init__(self, build_queue_client, broadcast_listener, git_repository,
            output):
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._git_repository = git_repository
        self._output = output

    def process(self, line):
        output = self._output
        output.write(line)
