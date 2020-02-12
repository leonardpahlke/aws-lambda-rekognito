import boto3
from main.config import *
from decimal import Decimal
from Util.Util import *

DYNAMO_DB_RESULTS = 'TableImageIndexResults'
DYNAMO_DB_CELEBS = 'TableImageIndexCelebrities'
USER_IMAGE_PATH_ID = 'user_imagepath_id'
CELEB_IMAGE_PATH_ID = 'celebrities_imagepath_id'

dynamo_db = boto3.resource('dynamodb', region_name='eu-central-1')
table_results = dynamo_db.Table(DYNAMO_DB_RESULTS)
table_celebs = dynamo_db.Table(DYNAMO_DB_CELEBS)

# STRUCTURE Table - Results
#   TableImageIndexResults: {
#       user_imagepath_id: <S> (S3-Filename) # key
#       s3_celeb_key: <S> (S3-Filename)
#       confidence: <N>
#   }

# STRUCTURE Table - Celebrities
#   TableImageIndexCelebrities: {
#       celebrities_imagepath_id: <S> (S3-Filename) # key
#       confidence: <N>
#       celebrity_name: celeb2-image <S>
#   }


# check if this celeb already exist - DynamoDB
def does_celeb_exist(name):
    s3_celeb_key = get_s3_key_from_name(name, CELEBRITIES_FOLDER)
    response = table_celebs.get_item(
        Key={
            CELEB_IMAGE_PATH_ID: s3_celeb_key
        }
    )
    # information is in response['Item'] << celeb name and s3-image key
    return response['Item'] if 'Item' in response else {}


# store new celebrity into dynamo db
def store_new_celeb(s3_celeb_key, confidence, celeb_name=''):
    if celeb_name == '':
        celeb_name = get_name_from_s3_key(s3_celeb_key)
    response = table_celebs.put_item(
        Item={
            CELEB_IMAGE_PATH_ID: s3_celeb_key,  # DB key
            'celebrity_name': celeb_name,
            'confidence': Decimal(confidence)
        }
    )
    return response


# get stored results from dynamoDB
def get_results(name):
    user_s3_key = get_s3_key_from_name(name, USER_FOLDER)
    response = table_results.get_item(
        Key={
            USER_IMAGE_PATH_ID: user_s3_key
        }
    )
    return response['Item'] if 'Item' in response else {}


# store new user match into dynamoDB - results
def store_results_in_dynamo_db(s3_user_key, s3_celeb_key, confidence):
    response = table_results.put_item(
        Item={
            USER_IMAGE_PATH_ID: s3_user_key,  # DB key
            's3_celeb_key': s3_celeb_key,
            'confidence': Decimal(confidence)
        })
    return response
