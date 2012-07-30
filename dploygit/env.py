import os
from . import constants


class GitoliteEnv(object):
    """An interface to the environment variables of gitolite"""
    @classmethod
    def load(cls, env=None):
        env = env or os.environ
        username = env.get('GL_USER')
        repository_name = env.get('GL_REPO')
        admin_base = env.get('GL_ADMIN_BASE')
        repositories_base = env.get('GL_REPO_BASE')
        lib_dir = env.get('GL_LIBDIR')
        bin_dir = env.get('GL_BINDIR')
        log_file = env.get('GL_LOGFILE')
        return cls(username, repository_name, admin_base,
                repositories_base, lib_dir, bin_dir, log_file)

    def __init__(self, username, repository_name, admin_base,
            repositories_base, lib_dir, bin_dir, log_file):
        self.username = username
        self.repository_name = repository_name
        self.admin_base = admin_base
        self.repositories_base = repositories_base
        self.lib_dir = lib_dir
        self.bin_dir = bin_dir
        self.log_file = log_file

    @property
    def custom_config_path(self):
        """A path to be used for custom configuration"""
        return os.path.join(self.admin_base, constants.CUSTOM_CONFIG)
