from google.cloud import storage
import os

bucket_name = "sweetroll-captured-images"
source_file_name = "cap_test.jpg"

client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(source_file_name)
blob.upload_from_filename(source_file_name)