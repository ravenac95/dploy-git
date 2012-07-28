from . import constants
from ConfigParser import ConfigParser


class GitReceiveUpdate(object):
    pass


class GitRepository(object):
    pass


class GitoliteEnv(object):
    pass


class PreReceiveProcessor(object):
    pass


class GitoliteHook(object):
    @classmethod
    def setup(cls):
        env = GitoliteEnv.load()
        git_repository = GitRepository.load(env.repository_name)
        config_path = env.custom_config_path
        config = ConfigParser()
        config.read(config_path)
        hook = cls(git_repository, env, config)

        # Run any custom initialization
        hook.initialize()
        return hook

    def __init__(self, git_repository, env, config):
        self._git_repository = git_repository
        self._env = env
        self._config = config


class BroadcastListener(object):
    pass


class BuildQueueClient(object):
    pass


class PreReceiveHook(GitoliteHook):
    """Pre-receive hook's start point"""
    def initialize(self):
        """Custom initialization for this hook"""
        queue_uri = self._config.get(constants.CONFIG_SECTION,
                'build-queue-uri')
        broadcast_listen_uri = self._config.get(constants.CONFIG_SECTION,
                'broadcast-listen-uri')

        self._build_queue_client = BuildQueueClient(queue_uri)
        self._broadcast_listener = BroadcastListener(broadcast_listen_uri)
        self._receive_processor = PreReceiveProcessor(self._build_queue_client,
                self._broadcast_listener, self._git_repository)

    def __init__(self, git_repository, env, config, build_queue_client=None,
            broadcast_listener=None, receive_processor=None):
        super(PreReceiveHook, self).__init__(git_repository, env, config)
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._receive_processor = receive_processor

    def run(self, input_file):
        """Run the hook"""
        for line in input_file:
            self._receive_processor.process(line)
