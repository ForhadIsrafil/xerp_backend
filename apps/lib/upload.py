import io
from PIL import Image
import hashlib
import tempfile
import shutil
from django.conf import settings
from os.path import join as pathjoin
import uuid
#from boto3.s3.key import Key
from urllib.parse import urljoin
#from boto3.s3.connection import S3Connection
import os
import boto3
from boto3.s3.transfer import S3Transfer

THUMBNAIL_SIDE_LIMIT = settings.THUMBNAIL_SIDE_LIMIT


# Here We were uploading a thumnail file (img)  and a ios file (model)

def upload_byte_file(file=None, model=None):
    filename = ''

    # Process the uploaded model
    _, ext = os.path.splitext(file.name)
    type = ext[1:].lower() if len(ext) > 0 else None

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tmppath = fp.name

        for chunk in file.chunks():
            fp.write(chunk)

        # Save the model in the static path
        hash = str(uuid.uuid4())
        filename = hash + '.' + type
        path = pathjoin(settings.FILE_ROOT, filename, )
        shutil.move(tmppath, path)

    return filename, hash

    # bucket_name = 'ashique-test-bucket'
    # aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    # aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY_ID
    #
    #
    # ## create connection to the service
    # conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    #
    # ## creating a bucket
    # bucket = conn.get_bucket(bucket_name)
def upload_file_s3(file=None, bucket_instance=None):
    # bucket_name = 'ashique-test-bucket'
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY_ID

    transfer = S3Transfer(boto3.client('s3', 'us-east-2',
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key))

    if bucket_instance:

        _, ext = os.path.splitext(file.name)
        type = ext[1:].lower() if len(ext) > 0 else None

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            tmppath = fp.name

    # local_directory = '/home/ashique00003/Desktop/sloop'
    # transfer = S3Transfer(boto3.client('s3', 'us-east-2',
    #                                    aws_access_key_id='AKIAVICL3GVQLWIKCKBY',
    #                                    aws_secret_access_key='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'))
    # client = boto3.client('s3')
    # for root, dirs, files in os.walk(local_directory):
    #     for filename in files:
    #         local_path = os.path.join(root, filename)
    #         # relative_path = os.path.relpath(local_path, local_directory)
    #         # s3_path = os.path.join('your s3 path',relative_path)
    #         transfer.upload_file(local_path, bucket.name, filename, extra_args={'ACL': 'public-read'})

    #return filename
            for chunk in file.chunks():
                fp.write(chunk)

            # Save the model in the static path
            hash = str(uuid.uuid4())
            filename = hash + '.' + type
            path = pathjoin(settings.FILE_ROOT, filename)
            shutil.move(tmppath, path)

            key = hash + ext

            transfer.upload_file(path, bucket_instance.name, key=key, extra_args={'ACL': 'public-read'})
            os.remove(path)

            return key
