import os
from contextlib import contextmanager


@contextmanager
def unset_virtualenv():
    _environ = os.environ.copy()
    try:
        os.environ.pop("VIRTUAL_ENV", None)
        yield
    finally:
        os.environ.clear()
        os.environ.update(_environ)
