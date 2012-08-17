from mock import patch
from dploygit.repository import *


def test_initialize_git_repository():
    name = 'name'
    git_dir = 'dir'
    repo = GitRepository(name, git_dir)
    assert repo.name == name
    assert repo.directory == git_dir


@patch('os.path.abspath')
def test_load_git_repository(mock_abspath):
    name = 'name'
    some_env = {'GIT_DIR': '/somedir'}
    repo = GitRepository.load(name, env=some_env)
    assert repo.name == name
    assert repo.directory == mock_abspath.return_value


class TestGitRepository(object):
    def setup(self):
        name = 'name'
        git_dir = 'dir'
        self.repository = GitRepository(name, git_dir)

    @patch('subwrap.run')
    def test_export_to_file(self, mock_run):
        export_path = 'ep.tar.gz'
        self.repository.export_to_file(export_path)
        mock_run.assert_called_with([
            'git', '--git-dir=dir', 'archive', '--prefix=name/',
            '--output=ep.tar.gz', 'HEAD'])
