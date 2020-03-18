from auto_smart_open.core import S3StorageBackend, FileStorageBackend
import os

backend = FileStorageBackend()

with backend.open('test.txt', 'w') as f:
    f.write('test')

S3_bucket = "test-smart-open-sg2020"
S3_key = os.environ['S3_KEY']
S3_secret = os.environ['S3_SECRET']

backend = S3StorageBackend(S3_bucket, S3_key, S3_secret)

with backend.open('new_file.txt', 'w') as f:
    f.write('test')