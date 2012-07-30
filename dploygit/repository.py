import os
import subwrap
import tempfile


class GitRepository(object):
    @classmethod
    def load(cls, name, env=None):
        env = env or os.environ
        git_dir = os.path.abspath(env['GIT_DIR'])
        return cls(name, git_dir)

    def __init__(self, name, directory):
        self._name = name
        self._directory = directory

    @property
    def name(self):
        return self._name

    @property
    def directory(self):
        return self._directory

    def export_to_file(self, destination, commit='HEAD'):
        """Exports the git repository to a specific file.

        The export format is determined by the destination's file extension
        """
        prefix_arg = '--prefix=%s/' % self.name
        output_arg = '--output=%s' % destination
        command = ['git', 'archive', prefix_arg, output_arg, commit]
        subwrap.run(command)
