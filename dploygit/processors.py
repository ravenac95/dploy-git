import requests
import json
from urlparse import urljoin
from .utils import make_temp_file_path


class DeployRequest(object):
    @classmethod
    def from_dict(cls, data):
        app = data['app']
        archive_uri = data['archive_uri']
        commit = data['commit']
        update_message = data['update_message']
        metadata_version = data['metadata_version']
        return cls(app, archive_uri, commit, update_message, metadata_version)

    @classmethod
    def from_update(cls, update, archive_uri, update_message):
        app = update.repository.name
        commit = update.new
        return cls(app, archive_uri, commit, update_message, 0)

    def __init__(self, app, archive_uri, commit, update_message,
            metadata_version):
        self.app = app
        self.archive_uri = archive_uri
        self.commit = commit
        self.update_message = update_message
        self.metadata_version = metadata_version

    def to_dict(self):
        return dict(app=self.app,
                archive_uri=self.archive_uri,
                commit=self.commit,
                update_message=self.update_message,
                metadata_version=self.metadata_version,
                )


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
            split_ref_name = self.ref_name.split('/')
            branch = split_ref_name[-1]
            self._branch = branch
        return self._branch

    def export_to_file(self):
        file_suffix = '.%s-%s.tar.gz' % (self.repository.name, self.new)
        file_path = make_temp_file_path(suffix=file_suffix)
        self.repository.export_to_file(file_path, commit=self.new)
        return file_path

    def pack_file(self, git_service_url):
        pack_request_data = dict(commit=self.new)
        headers = {'content-type': 'application/json'}

        pack_endpoint = "%s/pack" % self.repository.name

        pack_url = urljoin(git_service_url, pack_endpoint)
        print pack_url
        response = requests.post(pack_url,
                data=json.dumps(pack_request_data),
                headers=headers)
        return response.json['uri']


class PreReceiveProcessor(object):
    def __init__(self, build_queue_client, broadcast_listener, git_repository,
            output, git_service_uri):
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._git_repository = git_repository
        self._git_service_uri = git_service_uri
        self._output = output

    def process(self, line):
        output = self._output

        update = GitUpdate.from_line(line, self._git_repository)
        branch = update.branch
        if branch == 'master':
            output.line('Receiving new code from master branch')

            # Export the file to a temporary file
            update_file = update.pack_file(self._git_service_uri)

            # Create a DeployRequest
            update_message = '[USER] received new code commit hash "%s"' % \
                    update.new
            print "Update File: %s" % update_file
            print "Update Message: %s" % update_message
        else:
            output.line('Ignoring branch "%s"' % branch)
