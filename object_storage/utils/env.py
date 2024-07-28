import os
from ast import literal_eval

AWS_OBJECT_ENABLE = literal_eval(
    os.environ.get("AWS_OBJECT_ENABLE", "False")
)  # True or False
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME", "ap-southeast-1")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
