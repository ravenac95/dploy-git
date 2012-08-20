import os
import boto
from flask import Flask, abort, current_app, g, request, jsonify
from flaskcommand import flask_command
from repository import GitRepository
from utils import make_temp_file_path
#from .manager import DployGitManager
#from .models import PackRequest

app = Flask(__name__)


def app_factory(config_path):
    app.config.from_pyfile(config_path)
    return app


class S3Backend(object):
    def __init__(self, access_key, secret_key, bucket):
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket

    def upload(self, name, path):
        """Uploads a file to S3 and returns the url used for uploading"""
        # Create the connection
        connection = boto.connect_s3(self._access_key, self._secret_key)
        # Get the bucket
        bucket = connection.get_bucket(self._bucket)
        # Get the resource to the key
        key = bucket.new_key(name)
        # Upload the file
        key.set_contents_from_filename(path)
        # Generate an s3 url s3://bucket/key
        s3_uri = "s3://%s/%s" % (self._bucket, name)
        return s3_uri


class DployGitManager(object):
    def __init__(self, git_repos_path, storage_backend):
        self._git_repos_path = git_repos_path
        self._storage_backend = storage_backend

    def get_repository(self, repository_name):
        repository_git_name = '%s.git' % repository_name
        repository_path = os.path.join(self._git_repos_path,
                repository_git_name)
        return GitRepository(repository_name, repository_path)

    def pack_repository(self, repository_name, pack_request):
        commit = pack_request.commit
        repository = self.get_repository(repository_name)
        temp_path = make_temp_file_path(suffix='.tar.gz', prefix='dploy')
        repository.export_to_file(temp_path, commit=commit)
        context = dict(name=repository_name, commit=commit)
        key_name = "%(name)s/%(name)s-%(commit)s.tar.gz" % context
        uri = self._storage_backend.upload(key_name, temp_path)
        return uri


class GitPackRequest(object):
    @classmethod
    def deserialize(cls, raw_data):
        commit = raw_data['commit']
        return cls(commit)

    def __init__(self, commit):
        self._commit = commit

    @property
    def commit(self):
        return self._commit


@app.before_request
def load_git_manager():
    config = current_app.config
    storage_backend = S3Backend(config['AWS_ACCESS_KEY'],
            config['AWS_SECRET_KEY'], config['S3_BUCKET'])
    manager = DployGitManager(config['GIT_REPOS_PATH'], storage_backend)
    g.manager = manager


@app.route('/<repository>/pack', methods=["POST"])
def pack_repository(repository):
    json_data = request.json
    if not json_data:
        abort(400)
    pack_request = GitPackRequest.deserialize(json_data)
    pack_uri = g.manager.pack_repository(repository, pack_request)
    return jsonify(uri=pack_uri)


run = flask_command(factory=app_factory)

# For debugging
if __name__ == '__main__':
    import sys
    config_path = os.path.join(os.getcwd(), sys.argv[1])
    abs_config_path = os.path.abspath(config_path)
    app = app_factory(abs_config_path)
    app.run(debug=True)
