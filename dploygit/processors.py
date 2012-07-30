class GitUpdate(object):
    pass


class PreReceiveProcessor(object):
    def __init__(self, build_queue_client, broadcast_listener, git_repository,
            output):
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._git_repository = git_repository
        self._output = output

    def process(self, line):
        output = self._output

        update = GitUpdate.from_line(line)
        branch = update.branch
        if branch == 'master':
            output.line('Receiving new code from master branch')
            # Export the file to a temporary file
            update_file = update.export_to_file()
            # Queue the DeployRequest
            # Should receive a listening channel in the response
            response = self._build_queue_client.send_deploy_request(
                    self._git_repository.name, update_file)
            # Wait and listen to the broadcaster using the received
            # listening channel
            self._broadcast_listener.listen_from_response(response)
        else:
            output.line('Ignoring branch "%s"' % branch)
