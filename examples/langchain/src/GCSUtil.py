from google.cloud import storage
import os


class GCSUtil:

    def __init__(self):
        self.storage_client = storage.Client()

    def create_bucket(self, bucket_name, location="us", storage_class="STANDARD"):
        bucket = self.storage_client.bucket(bucket_name)
        bucket.storage_class = storage_class
        new_bucket = self.storage_client.create_bucket(bucket, location=location)

        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket

    def get_bucket(self, bucket_name):
        return self.storage_client.get_bucket(bucket_name)

    def get_bucket_matching(self, bucket_prefix):
        bucket_iterator = self.storage_client.list_buckets(prefix=bucket_prefix)
        buckets = []
        for bucket in bucket_iterator:
            buckets.append(bucket)
        return buckets

    def delete_bucket(self, bucket_name):
        print(f"Deleting bucket: {bucket_name}...")
        bucket = self.storage_client.get_bucket(bucket_name)
        bucket.delete(force=True)
        print(f"Bucket {bucket.name} deleted")

    def add_file(self, bucket_name, file_path):
        # Get the target bucket
        bucket = self.storage_client.bucket(bucket_name)

        # Upload the file to the bucket
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)