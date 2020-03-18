from abc import ABC, abstractmethod
from contextlib import contextmanager
from smart_open import open as s_open
import boto3


class Backend(ABC):
    """
    Abstract class to provide a configurable backends that will provide an open method
    """
    @abstractmethod
    def open(self, *args, **kwargs):
        pass


class S3StorageBackend(Backend):
    def __init__(self, s3_bucket, s3_key=None, s3_secret=None):
        """
        Just store the S3 credentials to pass it everytime an open is required
        """
        self._bucket = s3_bucket
        self._session = boto3.Session(
            aws_access_key_id=s3_key,
            aws_secret_access_key=s3_secret
        )
        
    @contextmanager
    def open(self, path, *args, **kwargs):
        s3_path = f"s3://{self._bucket}/{path}"
        with s_open(s3_path, transport_params=dict(session=self._session), *args, **kwargs) as context:
            yield context


class FileStorageBackend(Backend):
    def __init__(self):
        pass
    
    @contextmanager
    def open(self, path, *args, **kwargs):
        with s_open(path, *args, **kwargs) as context:
            yield context
        

    
