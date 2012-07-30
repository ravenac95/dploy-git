import sys
from .hooks import DployPreReceiveHook


def pre_receive():
    """Main entry point for dploygit pre-receive hook.

    Just run this inside a hook.
    """
    DployPreReceiveHook(sys.stdin)
