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

    def line(self, message=''):
        use_prefix = True
        if not message:
            # If it's an empty line don't include the prefix
            use_prefix = False
        self.write(message, use_prefix=use_prefix)
        self.new_line()

    def write(self, string, use_prefix=True):
        string = str(string)
        if self._on_new_line:
            self._output_stream.write(PRINT_PREFIX)
            prefix = self._prefix
            if not use_prefix:
                prefix = SPACE_PREFIX
            self._output_stream.write(prefix)
        string = string.replace('\n', NEWLINE_REPLACE)
        self._output_stream.write(string)
        self._output_stream.flush()
        self._on_new_line = False

    def new_line(self):
        self._on_new_line = True
        self._output_stream.write('\n')


def make_temp_file_path(suffix='', prefix=None, dir=None, text=False):
    """Simply creates a temporary file path"""
    options = dict(suffix=suffix, text=text)
    if prefix:
        options['prefix'] = prefix
    if dir:
        options['dir'] = dir
    file_handle, file_path = tempfile.mkstemp(**options)
    # Close the file
    os.close(file_handle)
    # Return the filename
    return file_path
