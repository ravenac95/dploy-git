import sys
from .hooks import DployPreReceiveHook


def pre_receive(input_file=None):
    """Main entry point for dploygit pre-receive hook.

    Just run this inside a hook.
    """
    input_file = input_file or sys.stdin
    hook = DployPreReceiveHook.setup()
    hook.run(input_file)
