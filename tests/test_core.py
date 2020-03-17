import pytest
from unittest.mock import MagicMock

from auto_smart_open.core import FileStorageBackend

class Mocker:
    def __enter__(self):
        return "entering context"
    def __exit__(self, type, value, traceback):
        raise FileNotFoundError

def test_sopen():
    """
    Replace the smart_open open with a mock function to see if __enter__ and __exit__ methods are properly called.
    """
    backend = FileStorageBackend()
    # mock the smart open open
    backend.open = MagicMock(return_value=Mocker())
    with pytest.raises(FileNotFoundError):
        with backend.open("test", "r") as f:
            assert f == "entering context"
        
