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


class TestDployPreReceiveHook(object):
    def setup(self):
        self.mock_repo = Mock()
        self.mock_env = Mock()
        self.mock_config = Mock()
        self.mock_build_queue_client = Mock()
        self.mock_broadcast_listener = Mock()
        self.mock_receive_processor = Mock()
        self.mock_output_stream = Mock()

        self.hook = DployPreReceiveHook(self.mock_repo, self.mock_env,
                self.mock_config, self.mock_output_stream,
                self.mock_build_queue_client,
                self.mock_broadcast_listener, self.mock_receive_processor)

    def test_run_build(self):
        # Setup mocks
        mock_input_file = MagicMock()
        mock_input_file.__iter__.return_value = iter(['a', 'b', 'c'])

        # Run Test
        exit_code = self.hook.run_build(mock_input_file)

        # Assertions
        expected_calls = [
            call('a'),
            call('b'),
            call('c'),
        ]
        self.mock_receive_processor.process.assert_has_calls(expected_calls)
        assert exit_code == 0

    def test_run(self):
        # Setup mocks
        mock_input_file = Mock()
        mock_repository_ok = self.hook.repository_ok = Mock()
        mock_run = self.hook.run_build = Mock()
        mock_repository_ok.return_value = True

        # Run Test
        self.hook.run(mock_input_file)

        # Assertions
        mock_run.assert_called_with(mock_input_file)

    def test_run_ignore_repository(self):
        # Setup mocks
        mock_repository_ok = self.hook.repository_ok = Mock()
        mock_run = self.hook.run_build = Mock()
        mock_repository_ok.return_value = False

        # Run Test
        self.hook.run(None)

        # Assertions
        message = 'The run_build method should not be called'
        assert mock_run.called == False, message

    def test_repository_ok(self):
        self.mock_config.get.return_value = "hello\nworld\nthere\n"

        self.mock_repo.name = 'something'
        assert self.hook.repository_ok() == True

    def test_repository_ok_returns_false(self):
        self.mock_config.get.return_value = "hello\nworld\nthere\n"

        self.mock_repo.name = 'hello'
        assert self.hook.repository_ok() == False

        self.mock_repo.name = 'world'
        assert self.hook.repository_ok() == False

        self.mock_repo.name = 'there'
        assert self.hook.repository_ok() == False
