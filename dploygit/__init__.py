import sys
from .hooks import PreReceiveHook


def pre_receive():
    """Main entry point for dploygit pre-receive hook.

    Just run this inside a hook.
    """
    PreReceiveHook(sys.stdin)
