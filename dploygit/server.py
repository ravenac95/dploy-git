import os
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


class DployGitManager(object):
    def __init__(self, git_repos_path):
        self._git_repos_path = git_repos_path

    def get_repository(self, repository_name):
        repository_git_name = '%s.git' % repository_name
        print "REPO NAME %s" % repository_git_name
        repository_path = os.path.join(self._git_repos_path,
                repository_git_name)
        print "REPO PATH %s" % repository_path
        return GitRepository(repository_name, repository_path)

    def pack_repository(self, repository_name, pack_request):
        commit = pack_request.commit
        repository = self.get_repository(repository_name)
        temp_path = make_temp_file_path(suffix='.tar.gz', prefix='dploy')
        repository.export_to_file(temp_path, commit=commit)
        return temp_path


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
    manager = DployGitManager(config['GIT_REPOS_PATH'])
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
