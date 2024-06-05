from google.cloud import storage
import datetime
import os

YOUR_ACCESS_KEY_ID = os.(YOUR_ACCESS_KEY_ID)
YOUR_SECRET_KEY = os.(YOUR_SECRET_KEY)

def generate_signed_url_with_token(bucket_name, object_name, access_key_id, secret_key):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    expiration = datetime.timedelta(hours=1)  # Set the expiration time
    token = blob.generate_signed_url(expiration=expiration, access_key_id=access_key_id, secret_access_key=secret_key)

    return token

# Replace these values with your bucket, object, access key ID, and secret key
bucket_name = 'supersetdb'
object_name = 'superset.db'
access_key_id = YOUR_ACCESS_KEY_ID
secret_key = YOUR_SECRET_KEY

signed_url_with_token = generate_signed_url_with_token(bucket_name, object_name, access_key_id, secret_key)
print("Signed URL with token:", signed_url_with_token)
