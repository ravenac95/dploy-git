import os
import sys
import tempfile

PRINT_PREFIX = '\b' * 8
MESSAGE_PREFIX = '------> '
SPACE_PREFIX = '        '
NEWLINE_REPLACE = '\n%s%s' % (PRINT_PREFIX, SPACE_PREFIX)


class HookOutputStream(object):
    """Wrapper around an output stream specifically for git ssh hooks"""
    def __init__(self, output_stream=None, prefix=MESSAGE_PREFIX):
        self._output_stream = output_stream or sys.stdout
        self._on_new_line = True
        self._prefix = prefix

    def line(self, message):
        self.write(message)
        self.new_line()

    def write(self, string):
        if self._on_new_line:
            self._output_stream.write(PRINT_PREFIX)
            self._output_stream.write(self._prefix)
        string = string.replace('\n', NEWLINE_REPLACE)
        self._output_stream.write(string)
        self._on_new_line = False

    def new_line(self):
        self._on_new_line = True
        self._output_stream.write('\n')


def make_temp_file_path(suffix='', prefix=''):
    """Simply creates a temporary file path"""
    file_handle, file_path = tempfile.mkstemp()
    # Close the file
    os.close(file_handle)
    # Return the filename
    return file_path
