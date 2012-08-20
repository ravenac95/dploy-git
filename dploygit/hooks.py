from ConfigParser import ConfigParser
from . import constants
from .utils import HookOutputStream
from .env import GitoliteEnv
from .processors import *
from .broadcastlistener import *
from .queueclient import *
from .repository import *
from .appserviceclient import *


class GitoliteHook(object):
    @classmethod
    def setup(cls):
        env = GitoliteEnv.load()
        git_repo = GitRepository.load(env.repository_name)
        config_path = env.custom_config_path
        config = ConfigParser()
        config.read(config_path)
        output_stream = HookOutputStream()
        hook = cls(git_repo, env, config, output_stream)

        # Run any custom initialization
        hook.initialize()
        return hook

    def __init__(self, git_repo, env, config, output):
        self._git_repo = git_repo
        self._env = env
        self._config = config
        self._output = output


class DployPreReceiveHook(GitoliteHook):
    """Pre-receive hook's start point"""
    def initialize(self):
        """Custom initialization for this hook"""
        config = dict(self._config.items(constants.CONFIG_SECTION))
        queue_uri = config['build-queue-uri']
        broadcast_listen_uri = config['broadcast-listen-uri']
        git_service_uri = config['git-service-uri']
        app_service_uri = config['app-service-uri']
        app_service_client = AppServiceClient(app_service_uri)

        self._build_queue_client = BuildQueueClient(queue_uri)
        self._broadcast_listener = BroadcastListener(broadcast_listen_uri,
                self._output)
        self._receive_processor = PreReceiveProcessor(self._build_queue_client,
                self._broadcast_listener, self._git_repo,
                git_service_uri, app_service_client, self._output)

    def __init__(self, git_repo, env, config, output,
            build_queue_client=None,
            broadcast_listener=None, receive_processor=None):
        super(DployPreReceiveHook, self).__init__(git_repo, env, config,
                output)
        self._build_queue_client = build_queue_client
        self._broadcast_listener = broadcast_listener
        self._receive_processor = receive_processor

    def run(self, input_file):
        """Run the hook"""
        output = self._output
        output.line()
        if self.repository_ok():
            self.run_build(input_file)
        output.line()

    def run_build(self, input_file):
        output = self._output
        output.line('dploy preparing to receive app for build')
        exit_code = 0
        try:
            for line in input_file:
                self._receive_processor.process(line)
        except:
            output.line("An error during the app's build process")
            exit_code = 1
            raise
        else:
            output.line('dploy completed task successfully!')
        return exit_code

    def repository_ok(self):
        """Ignores repositories based on configuration"""
        # This is most useful for ignoring gitolite-admin so it doesn't get
        # built
        raw_ignore_list = self._config.get(constants.CONFIG_SECTION,
                'repo-ignore-list')
        ignore_list = raw_ignore_list.splitlines()
        repository_name = self._git_repo.name
        if repository_name in ignore_list:
            self._output.line('dploy ignoring repository "%s"' %
                    repository_name)
            return False
        return True
