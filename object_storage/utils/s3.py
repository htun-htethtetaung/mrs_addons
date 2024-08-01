import logging
import hashlib
import boto3
from botocore.exceptions import ClientError
from .env import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION_NAME,
    AWS_BUCKET_NAME,
    AWS_OBJECT_ENABLE,
)

_logger = logging.getLogger(f"{__name__} : #S3")


def retry_func(retry: int = 1):
    def inner_func_parent(func):
        def inner_func(*args, **kwargs):
            for count in range(1, retry + 1):
                try:
                    return func(*args, **kwargs)
                except ClientError as err:
                    if count < retry:
                        continue
                    raise err

        return inner_func

    return inner_func_parent


class S3ContextMgr:
    def __init__(self) -> None:
        self.bucket_name = AWS_BUCKET_NAME
        self.session = boto3.session.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION_NAME,
        )
        self.client = self.session.client("s3")
        if AWS_OBJECT_ENABLE:
            try:
                self.client.head_bucket(Bucket=self.bucket_name)
                _logger.info("Bucket Name %s is already exist.", self.bucket_name)
            except ClientError as err:
                if (
                    err.response.get("Error")
                    and err.response["Error"].get("Code") == "404"
                ):
                    self.client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": AWS_REGION_NAME
                        },
                    )
                    _logger.info(
                        "Bucket Name %s is successfully created.", self.bucket_name
                    )

    # pylint: disable=too-many-arguments
    @retry_func(retry=2)
    def put_object(
        self,
        data: bytes,
        filename: str,
        key: str = None,
        bucket_name: str = AWS_BUCKET_NAME,
        content_type: str = "application/octet-stream",
        metadata: dict = None,
    ) -> str:
        """Update data to s3

        Args:
            data (bytes): file data
            filename (str):  Defaults to "it is for download from s3".
            key (str): Defaults to checksum value.
            bucket_name (str, optional):  Defaults to AWS_BUCKET_NAME.
            content_type (str, optional):  Defaults to "application/octet-stream".
            metadata (dict, optional):  Defaults to None.

        Returns:
            str: filename or checksum value
        """
        if not key:
            key = hashlib.sha1(data or b"").hexdigest()
        metadata = {} if metadata is None else metadata
        metadata.update({"filename": filename, "key": key})
        with self as s3_mgr:
            s3_mgr.client.put_object(
                Bucket=bucket_name,
                Body=data,
                Key=key,
                ContentType=content_type,
                Metadata=metadata,
                ContentDisposition=filename,
            )
        return key

    @retry_func(retry=2)
    def delete_object(self, key: str, bucket_name: str = AWS_BUCKET_NAME):
        """Delete object from s3

        Args:
            key (str): object key
            bucket_name (str, optional): _description_. Defaults to AWS_BUCKET_NAME.
        """
        with self as s3_mgr:
            s3_mgr.client.delete_object(
                Bucket=bucket_name,
                Key=key,
            )

    @retry_func(retry=2)
    def get_object(self, key: str, bucket_name: str = AWS_BUCKET_NAME):
        """Get object from s3

        Args:
            key (str): object key
            bucket_name (str, optional): _description_. Defaults to AWS_BUCKET_NAME.
        """
        with self as s3_mgr:
            response = s3_mgr.client.get_object(Bucket=bucket_name, Key=key)
            return response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_traceback:
            self.session = boto3.session.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION_NAME,
            )
            self.client = self.session.client("s3")


s3 = S3ContextMgr()
