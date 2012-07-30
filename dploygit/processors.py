import tempfile


class GitUpdate(object):
    @classmethod
    def from_line(cls, line, repository):
        stripped_line = line.strip()
        args = stripped_line.split(' ')
        args.append(repository)
        return cls(*args)

    def __init__(self, old, new, ref_name, repository):
        self._old = old
        self._new = new
        self._ref_name = ref_name
        self._repository = repository
        self._branch = None

    @property
    def old(self):
        return self._old

    @property
    def new(self):
        return self._new

    @property
    def ref_name(self):
        return self._ref_name

    @property
    def repository(self):
        return self._repository

    @property
    def branch(self):
        """Returns a simple branch name"""
        branch = self._branch
        if not branch:
            split_ref_name = self._ref_name.split('/')
            branch = split_ref_name[-1]
            self._branch = branch
        return self._branch

    def export_to_file(self):
        export_dir = tempfile.mkdtemp()
        self.repository.checkout_to_dir(export_dir, commit=self.new)
        return export_dir


class PreReceiveProcessor(object):
    def __init__(self, build_queue_client, broadcast_listener, git_repository,
            output):
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._git_repository = git_repository
        self._output = output

    def process(self, line):
        output = self._output

        update = GitUpdate.from_line(line, self._git_repository)
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
