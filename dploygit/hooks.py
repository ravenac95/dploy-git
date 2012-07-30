import sys
from ConfigParser import ConfigParser
from . import constants
from .utils import HookOutputStream


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
        output_stream = HookOutputStream()
        hook = cls(git_repository, env, config, output_stream)

        # Run any custom initialization
        hook.initialize()
        return hook

    def __init__(self, git_repository, env, config, output):
        self._git_repository = git_repository
        self._env = env
        self._config = config
        self._output = output


class BroadcastListener(object):
    pass


class BuildQueueClient(object):
    pass


class DployPreReceiveHook(GitoliteHook):
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
                self._broadcast_listener, self._git_repository,
                self._output)

    def __init__(self, git_repository, env, config, output, build_queue_client,
            broadcast_listener, receive_processor):
        super(DployPreReceiveHook, self).__init__(git_repository, env, config,
                output)
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._receive_processor = receive_processor

    def run(self, input_file):
        """Run the hook"""
        output = self._output
        output.line('dploy ready to receive')
        try:
            for line in input_file:
                self._receive_processor.process(line)
        except:
            raise
            output.line('An error during the build hook')
            sys.exit(1)
        output.line('dploy completed successfully!')
