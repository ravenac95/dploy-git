from mock import Mock, MagicMock, patch, call
from dploygit.hooks import *


def test_initialize_pre_receive_hook():
    PreReceiveHook(None)


def mock_update(branch):
    mock_obj = Mock(name='GitReceiveUpdate:%s' % branch)
    mock_obj.branch = branch
    return mock_obj


class TestPreReceiveHook(object):
    def setup(self):
        self.mock_stdin = MagicMock(name='stdin')
        self.mock_dploy_center_client =

        self.git_receive_update_cls_patch = patch(
                'dploygit.hooks.GitReceiveUpdate', new=Mock())
        self.mock_git_receive_update_cls = \
                self.git_receive_update_cls_patch.start()

        self.mock_git_repository = Mock()

        self.gitolite_env_cls_patch = patch(
                'dploygit.hooks.GitReceiveUpdate', new=Mock())
        self.mock_git_receive_update_cls = \
                self.git_receive_update_cls_patch.start()

        self.hook = PreReceiveHook(self.git_repository, 'user', 'repo',
                mock_updates, self.mock_dploy_center_client)

    def teardown(self):
        self.git_receive_update_cls_patch.stop()
        self.git_repository_patch.stop()

    def test_run(self):
        # Setup updates
        mock_master = mock_update('master')
        fake_updates = [
            mock_update('some'),
            mock_update('other'),
            mock_master,
        ]
        self.mock_stdin.__iter__.return_value = iter(['a', 'b', 'c'])
        self.mock_git_receive_update_cls.from_line.side_effect = fake_updates

        # Run Test
        self.hook.run()

        # Assertions
        expected_calls = [
            call('a', self.mock_git_repository),
            call('b', self.mock_git_repository),
            call('c', self.mock_git_repository),
        ]
        self.mock_git_receive_update_cls.from_line.assert_has_calls(
                expected_calls)
        mock_master.export_to_file.assert_called_with()
