from Util.Util import *
from main.config import *
from Util.UtilS3 import create_pre_signed_url, does_key_exist

'''
Get images from S3 bucket to display them in frontend
Services: S3 - source images
return image download url
'''


class GetSourceImage(MethodAction):
    def set_method(self):
        self.http_method = GET
        self.option = 'source-image'

    def execute(self, message):
        # TODO message['message']
        message = message['message']

        # check if message parameter are set
        if 'celebrity' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[GetSourceImage] parameter celebrity not set')
        if 'request' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[GetSourceImage] parameter request not set')
        is_celebrity_requested = message['celebrity']
        object_reference_requested = message['request']

        folder = CELEBRITIES_FOLDER if is_celebrity_requested == 'True' else USER_FOLDER
        s3_key = get_s3_key_from_name(object_reference_requested, folder)
        if does_key_exist(s3_key):
            url = create_pre_signed_url(s3_key)
            return set_response(
                self.response,
                log='[GetSourceImage] url is ready',
                message='Download Image',
                data=url
            )
        else:
            return set_response(
                self.response,
                message='Image not found',
                log='[GetSourceImage] image not in s3 bucket',
                data={'success': False}
            )
