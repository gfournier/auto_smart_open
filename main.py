from auto_smart_open.core import S3StorageBackend, FileStorageBackend

backend = FileStorageBackend()

with backend.open('test.txt', 'w') as f:
    f.write('test')

S3_bucket = "test-smart-open-sg2020"
S3_key = ""
S3_secret = ""

backend = S3StorageBackend(S3_bucket, S3_key, S3_secret)

with backend.open('test.txt', 'w') as f:
    f.write('test')