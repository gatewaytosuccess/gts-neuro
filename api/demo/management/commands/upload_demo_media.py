"""Run once by hand. ``seed_demo --reset`` points at these keys but never uploads them."""

from django.conf import settings
from django.core.management.base import BaseCommand

from common import storage
from demo import assets


class Command(BaseCommand):
    help = "Upload api/demo/media/ to the demo's fixed keys in both buckets."

    def handle(self, *args, **options):
        for asset in assets.ALL:
            bucket = (
                settings.AWS_PRIVATE_BUCKET_NAME
                if asset.private
                else settings.AWS_THUMBNAIL_BUCKET_NAME
            )
            storage.upload_file(bucket, asset.key, asset.path, asset.content_type)
            self.stdout.write(f"s3://{bucket}/{asset.key}")
        self.stdout.write(self.style.SUCCESS(f"Uploaded {len(assets.ALL)} files."))
