from mock import Mock, patch
from dploygit.utils import *


class TestMakeTempFilePath(object):
    def setup(self):
        # Setup patches
        self.os_close_patch = patch('os.close')
        self.mock_os_close = self.os_close_patch.start()

        self.mkstemp_patch = patch('tempfile.mkstemp')
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
