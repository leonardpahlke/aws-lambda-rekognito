import re
from abc import ABC, abstractmethod
from PIL import Image
from main.config import *

JPG = '.jpg'
S3_KEY_NAME_REGEX = '.*\/(.*)\..*'

STATUS_CODE = "statusCode"
BODY = "body"
QUERY_STRING_PARAMS = 'queryStringParameters'

MESSAGE = "message"
OPTION = 'option'
LOG = 'log'
DATA = 'data'
METHOD = 'httpMethod'

# rest-api response codes
OK = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404

# http methods
GET = 'GET'
HEAD = 'HEAD'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
CONNECT = 'CONNECT'
OPTIONS = 'OPTIONS'
TRACE = 'TRACE'
PATCH = 'PATCH'

HTTP_METHODS = [GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH]

# default response
DEFAULT_RESPONSE = {
    STATUS_CODE: OK,
    BODY: {
        LOG: "",
        DATA: "",
        MESSAGE: ""
    }
}

DEFAULT_BAD_RESPONSE = DEFAULT_RESPONSE.copy()
DEFAULT_BAD_RESPONSE[STATUS_CODE] = BAD_REQUEST
DEFAULT_BAD_RESPONSE[BODY][MESSAGE] = 'request failed'
DEFAULT_BAD_RESPONSE[BODY][LOG] = 'unsupported request method'

DEFAULT_NOT_FOUND_RESPONSE = DEFAULT_RESPONSE.copy()
DEFAULT_NOT_FOUND_RESPONSE[STATUS_CODE] = NOT_FOUND
DEFAULT_NOT_FOUND_RESPONSE[BODY][MESSAGE] = 'request failed'
DEFAULT_NOT_FOUND_RESPONSE[BODY][LOG] = 'request could not be found'


class RDSConfig:
    db_user = RDS_USERNAME
    db_password = RDS_PASSWORD
    db_host = RDS_ENDPOINT
    db_port = RDS_PORT
    db_name = RDS_NAME


class MethodAction(ABC):
    http_method = None
    option = None
    response = None

    def __init__(self):
        # set method-action variables
        # example: http_method = 'GET', option = 'source-images'
        self.set_method()
        if not HTTP_METHODS.__contains__(self.http_method):
            raise AttributeError('Util.py - http method: {} unrecognized'.format(self.http_method))
        response = DEFAULT_RESPONSE
        self.response = response

    @abstractmethod
    def set_method(self):
        pass

    @abstractmethod
    def execute(self, message):
        pass


def b64_test_image():
    import os
    abs_path = os.path.abspath('./Util/bernie-sanders.jpg')
    with open(abs_path, 'rb') as image:
        return image.read()


def convert_hex_to_file(name, image_data):
    fh = open(name, 'w')
    return fh.write(image_data)


def get_s3_key_from_name(name, folder):
    return folder + '/' + name.replace(' ', '-') + JPG


def get_name_from_s3_key(s3_key):
    # 'celebrities/Michael-Jackson.jpg' -> x[1]: Michael-Jackson
    return re.search(S3_KEY_NAME_REGEX, s3_key)[1]


def set_response(response, status_code='', message='', log='', data=''):
    if status_code != '':
        response[STATUS_CODE] = status_code
    if message != '':
        response[BODY][MESSAGE] = message
    if log != '':
        response[BODY][LOG] = log
    if data != '':
        response[BODY][DATA] = data
    return response


def resize_image(image_data, max_width=800, max_height=800):
    stream = BytesIO(image_data)
    image = Image.open(stream).convert('RGBA')
    (image_width, image_height) = image.size
    difference_width = max_width - image_width
    difference_height = max_height - image_height
    # image size > max_width and/or max_height
    if (difference_width < 0) or (difference_height < 0):
        # calculate reduce percentage, width & height
        if difference_width < difference_height:
            reduce_percentage = 1. - (abs(difference_width) / image_width)
        else:
            reduce_percentage = 1. - (abs(difference_height) / image_height)
        # reduce image size
        image = image.resize(
            (int(image_width * reduce_percentage), int(image_height * reduce_percentage)),
            Image.ANTIALIAS
        )
    return image
