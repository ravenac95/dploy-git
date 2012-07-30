from mock import Mock, patch
from dploygit.processors import *


class TestPreReceiveProcessor(object):
    def setup(self):
        # Setup Basic Mocks
        self.mock_build_queue_client = Mock()
        self.mock_broadcast_listener = Mock()
        self.mock_git_repo = Mock()
        self.mock_output = Mock()

        # Setup Patches
        self.git_update_cls = patch('dploygit.processors.GitUpdate',
                autospec=True)
        self.mock_git_update_cls = self.git_update_cls.start()

        # Setup object under test
        self.processor = PreReceiveProcessor(self.mock_build_queue_client,
                self.mock_broadcast_listener, self.mock_git_repo,
                self.mock_output)

    def teardown(self):
        self.git_update_cls.stop()

    def test_pre_receive_processor_process_master(self):
        # Setup
        mock_line = Mock()
        mock_git_update = self.mock_git_update_cls.from_line.return_value
        mock_git_update.branch = 'master'

        # Run Test
        self.processor.process(mock_line)

        # Assertions
        self.mock_git_update_cls.from_line.assert_called_with(mock_line,
                self.mock_git_repo)
        message = "GitUpdate.export_to_file not called"
        assert mock_git_update.export_to_file.called == True, message
        self.mock_build_queue_client.send_deploy_request.assert_called_with(
                self.mock_git_repo.name,
                mock_git_update.export_to_file.return_value)

    def test_pre_receive_processor_process_not_master(self):
        # Setup
        mock_line = Mock()
        mock_git_update = self.mock_git_update_cls.from_line.return_value
        mock_git_update.branch = 'somethingelse'

        # Run Test
        self.processor.process(mock_line)

        # Assertions
        message = "GitUpdate.export_to_file was called for some reason"
        assert mock_git_update.export_to_file.called == False, message


def test_git_update_from_line_many_times():
    line1 = 'abcdef1234 abcdef1235 refs/heads/master'
    expected1 = ['abcdef1234', 'abcdef1235', 'refs/heads/master', 'master']
    line2 = 'ghijkl1234 ghijkl1235 refs/heads/master'
    expected2 = ['ghijkl1234', 'ghijkl1235', 'refs/heads/master', 'master']
    line3 = 'ghijkl1234 ghijkl1236 refs/heads/tester'
    expected3 = ['ghijkl1234', 'ghijkl1236', 'refs/heads/tester', 'tester']

    tests = [
        (line1, expected1),
        (line2, expected2),
        (line3, expected3),
    ]
    mock_repo = Mock()

    for line, expected in tests:
        yield do_git_update_from_line, line, expected, mock_repo


def do_git_update_from_line(line, expected, mock_repo):
    update = GitUpdate.from_line(line, mock_repo)
    assert update.old == expected[0]
    assert update.new == expected[1]
    assert update.ref_name == expected[2]
    assert update.branch == expected[3]
    assert update.repository == mock_repo


class TestGitUpdate(object):
    def setup(self):
        self.mock_repo = Mock()

        self.mkdtemp_patch = patch('tempfile.mkdtemp', autospec=True)
        self.mock_mkdtemp = self.mkdtemp_patch.start()

        self.update = GitUpdate('abc', 'def', 'refs/heads/name',
                self.mock_repo)

    def teardown(self):
        self.mkdtemp_patch.stop()

    def test_export_to_file(self):
        update_file = self.update.export_to_file()

        # Assertions
        mock_temp_dir = self.mock_mkdtemp.return_value
        self.mock_repo.checkout_to_dir.assert_called_with(mock_temp_dir, commit='def')
        assert update_file == mock_temp_dir
