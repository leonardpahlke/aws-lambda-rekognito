import boto3
from botocore.errorfactory import ClientError

from Util.Util import *

DEFAULT_EXPIRATION = 3600

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


def update_celeb_image(name, image):
    s3_key = get_s3_key_from_name(name, CELEBRITIES_FOLDER)
    response_delete = s3_client.delete_object(Bucket=IMAGE_SOURCE_BUCKET, Key=s3_key)
    response_upload = upload_image(name, CELEBRITIES_FOLDER, image)
    return response_delete, response_upload


def upload_image(name, folder, image_data, bucket=IMAGE_SOURCE_BUCKET):
    image_data = resize_image(image_data)
    s3_key = get_s3_key_from_name(name, folder)
    s3_client.put_object(Bucket=bucket, Body=image_data, Key=s3_key)
    return s3_key


# return generator object which returns s3 bucket keys of celeb files
def give_me_celeb_picture_keys():
    bucket = s3.Bucket(IMAGE_SOURCE_BUCKET)
    for obj in bucket.objects.filter(Prefix=CELEBRITIES_FOLDER + '/'):
        yield obj.key


def does_key_exist(s3_key, bucket=IMAGE_SOURCE_BUCKET):
    try:
        s3.Object(bucket, s3_key).load()
    except ClientError as e:
        # the object does not exist else something went wrong - raise error typically
        return False if e.response['Error']['Code'] == "404" else e.response['Error']['Code']
    else:
        return True


def create_pre_signed_url(object_key, bucket=IMAGE_SOURCE_BUCKET, expiration=DEFAULT_EXPIRATION):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_key},
        ExpiresIn=expiration
    )
