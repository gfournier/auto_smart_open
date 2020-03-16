from abc import ABC, abstractmethod
from contextlib import contextmanager
from smart_open import open as sopen
import boto3

class Backend(ABC):
    """
    Abstract class to provide a configurable backends that will provide an open method
    """
    @abstractmethod
    def open(self):
        pass

class S3StorageBackend(Backend):
    def __init__(self, S3_bucket, S3_key=None, S3_secret=None, certificate=None):
        """
        Just store the S3 credentials to pass it everytime an open is required
        """
        self._bucket = S3_bucket
        self._session = boto3.Session(
            aws_access_key_id=S3_key,
            aws_secret_access_key=S3_secret
        )
        
    @contextmanager
    def open(self, path, *args, **kwargs):
        s3_path = f"s3://{self._bucket}/{path}"
        context = sopen(s3_path, transport_params=dict(session=self._session), *args, **kwargs)
        try:
            yield context
        finally:
            context.close()

class FileStorageBackend(Backend):
    def __init__(self):
        pass
    
    @contextmanager
    def open(self, path, *args, **kwargs):
        context = sopen(path, *args, **kwargs)
        try:
            yield context
        finally:
            context.close()
        

    
