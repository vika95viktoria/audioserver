from google.cloud import storage


def upload_to_bucket(blob_name, path_to_file, bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    return f"gs://{bucket_name}/{blob_name}"


def delete_file(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete_blob(file_name)
    return f'{file_name} deleted from bucket.'