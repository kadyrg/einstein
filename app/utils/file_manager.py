import boto3
from starlette.concurrency import run_in_threadpool
from fastapi import UploadFile, HTTPException
from app.core import settings
from uuid import uuid4
from starlette.responses import StreamingResponse
from botocore.exceptions import ClientError


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


class FileManager:
    def __init__(self, allowed_formats):
        self.access_key_id = settings.R2_ACCOUNT_ACCESS_KEY
        self.secret_access_key = settings.R2_ACCOUNT_SECRET_KEY
        self.endpoint_url = settings.ENDPOINT_URL

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            endpoint_url=self.endpoint_url
        )

        self.s3_client = s3_client

        self.allowed_formats = allowed_formats

        self.bucket = settings.BUCKET_NAME


    def _upload_to_r2_sync(self, bucket: str, key: str, body: bytes, content_type: str):
        self.s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
        )


    def _get_from_r2_sync(self, bucket: str, key: str) -> dict:
        return self.s3_client.get_object(
            Bucket=bucket,
            Key=key
        )


    async def upload_file(self, file: UploadFile, folder: str) -> str:

        if file.content_type not in self.allowed_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {file.content_type}. Allowed: {', '.join(self.allowed_formats)}"
            )

        bucket = self.bucket

        ext = file.filename.split(".")[-1]
        name = f"{folder}/{uuid4().hex}.{ext}"
        content = await file.read()

        await run_in_threadpool(
            self._upload_to_r2_sync,
            bucket,
            name,
            content,
            file.content_type,
        )

        return f"/{name}"


    async def get_image(self, filename: str):
        bucket = self.bucket

        try:
            image = await run_in_threadpool(self._get_from_r2_sync, bucket, filename)
            return StreamingResponse(image["Body"], media_type=image["ContentType"])

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "NoSuchKey":
                raise HTTPException(status_code=404, detail="Image not found")

            raise HTTPException(status_code=500, detail=f"R2 Error: {error_code}")


course_image_manager = FileManager(
    allowed_formats=ALLOWED_IMAGE_TYPES
)
