from mock import Mock, MagicMock, patch, call
from dploygit.hooks import *


class FakeGitoliteHook(GitoliteHook):
    def __init__(self, *args, **kwargs):
        super(FakeGitoliteHook, self).__init__(*args, **kwargs)
        self._initialized = False

    def assert_setup_data(self, git_repository, env, config):
        assert self._git_repository == git_repository, \
                "Git repository does not match"

        assert self._env == env, "Env does not match"

        assert self._config == config, "Config does not match"

        assert self._initialized, "Not Initialized"

    def initialize(self):
        self._initialized = True


@patch('dploygit.hooks.ConfigParser')
@patch('dploygit.hooks.GitoliteEnv')
@patch('dploygit.hooks.GitRepository')
def test_fake_hook(mock_repo_cls, mock_env_cls, mock_config_cls):
    mock_repo = mock_repo_cls.load.return_value
    mock_env = mock_env_cls.load.return_value
    mock_config = mock_config_cls.return_value

    hook = FakeGitoliteHook.setup()

    hook.assert_setup_data(mock_repo, mock_env, mock_config)

    mock_repo_cls.load.assert_called_with(mock_env.repository_name)
    mock_config.read.assert_called_with(mock_env.custom_config_path)


class TestPreReceiveHook(object):
    def setup(self):
        self.mock_repo = Mock()
        self.mock_env = Mock()
        self.mock_config = Mock()
        self.mock_build_queue_client = Mock()
        self.mock_broadcast_listener = Mock()
        self.mock_receive_processor = Mock()

        self.hook = PreReceiveHook(self.mock_repo, self.mock_env,
                self.mock_config, self.mock_build_queue_client,
                self.mock_broadcast_listener, self.mock_receive_processor)

    def test_run(self):
        # Setup mocks
        mock_input_file = MagicMock()
        mock_input_file.__iter__.return_value = iter(['a', 'b', 'c'])

        # Run Test
        self.hook.run(mock_input_file)

        # Assertions
        expected_calls = [
            call('a'),
            call('b'),
            call('c'),
        ]
        self.mock_receive_processor.process.assert_has_calls(expected_calls)
