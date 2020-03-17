import pytest
from unittest.mock import patch

from auto_smart_open.core import FileStorageBackend

class Mocker:
    def __enter__(self):
        print("entering context")
        return "entering context"
    def __exit__(self, type, value, traceback):
        raise FileNotFoundError

@patch('smart_open.open')
def test_sopen(patched_sopen):
    """
    Replace the smart_open open with a mock function to see if __enter__ and __exit__ methods are properly called.
    """
    print("test")
    backend = FileStorageBackend()
    # mock the smart open open
    patched_sopen.return_value = Mocker()
    with pytest.raises(FileNotFoundError):
        with backend.open("test", "r") as f:
            assert f == "entering context"