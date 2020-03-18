import pytest
from unittest.mock import patch
from contextlib import contextmanager

from auto_smart_open.core import FileStorageBackend, S3StorageBackend


class SimpleMocker:
    """
    Simple mocking class to test triggers on __enter__ and __exit__
    """
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        print("entering context")
        return "entering context"

    def __exit__(self, type, value, traceback):
        raise FileNotFoundError


@contextmanager
def fake_s_open(path, *args, **kwargs):
    """
    Simple mocking method that returns the parameters that were send
    """
    yield dict(path=path, args=args, kwargs=kwargs)


@patch('auto_smart_open.core.s_open', new=SimpleMocker)
def test_sopen():
    """
    Replace the smart_open open with a mock function to see if __enter__ and __exit__ methods are properly called.
    """
    backend = FileStorageBackend()

    # if its raises, it means __exit__ is called, and the resource is released
    with pytest.raises(FileNotFoundError):
        with backend.open("unknonw_file", "r") as f:
            # if true, __enter__ is called
            assert f == "entering context"


@patch('auto_smart_open.core.s_open', new=fake_s_open)
def test_proper_backend_called():
    """
    Check if depending on the backend called the correct parameters are send to s_open
    """
    path = "/test/file"

    # FileStorage
    backend = FileStorageBackend()
    with backend.open(path, "rb") as f:
        assert isinstance(f, dict)
        assert f['path'] == path
        assert 'rb' in f['args']

    # S3Storage
    # patch the s3 Session do prevent creating a real connection to S3
    with patch('auto_smart_open.core.boto3.Session', new=lambda *args, **kwargs: "new s3 session"):
        backend = S3StorageBackend("fake_bucket", "fake_key", "fake_secret")
        with backend.open(path, "rb") as f:
            assert isinstance(f, dict)
            assert f['path'] == f"s3://fake_bucket/{path}"
            assert f['kwargs']['transport_params']['session'] == "new s3 session"

