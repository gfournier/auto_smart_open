# auto_smart_open - configurable backends for smart_open

## Why ?

Our goal is to have reconfigurable backends for manipulating files within an application.

You write the code once, then run it with a local file system backend or switch to a S3 backend when deploying in production.

All interactions are backed by [smart_open](https://github.com/RaRe-Technologies/smart_open) library.

The `open` method of backends acts as a dropin of native `open`python function.

```python
from auto_smart_open import S3, FileSystem

# Open an S3 bucket
backend = S3(bucket='test', **credentials)

# Read some text file
with backend.open('/path/to/my/resource.txt', 'rt') as f:
  for line in f:
    print(repr(line))
    
# Use a local directory
backend_local = FileSystem(root='/home/user/data')

# Write a text file
with backend_local.open('myfile.txt', 'wt') as f:
  f.write('Hello World')
```
