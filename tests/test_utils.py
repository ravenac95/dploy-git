from mock import Mock, patch
from dploygit.utils import *


class TestMakeTempFilePath(object):
    def setup(self):
        # Setup patches
        self.os_close_patch = patch('os.close')
        self.mock_os_close = self.os_close_patch.start()

        self.mkstemp_patch = patch('tempfile.mkstemp', autospec=True)
        self.mock_mkstemp = self.mkstemp_patch.start()
        self.mock_temp_file_handle = Mock()
        self.mock_temp_file_path = Mock()
        self.mock_mkstemp.return_value = [self.mock_temp_file_handle,
                self.mock_temp_file_path]

        # There is no actual object under test other than
        # the function. So need to have that here

    def teardown(self):
        self.os_close_patch.stop()
        self.mkstemp_patch.stop()

    def test_make_temp_file_path(self):
        temp_path = make_temp_file_path()
        assert temp_path == self.mock_temp_file_path

    def test_make_temp_file_path_with_suffix_and_prefix(self):
        make_temp_file_path(suffix='s', prefix='p')

        self.mock_mkstemp.assert_called_with(suffix='s', prefix='p')

