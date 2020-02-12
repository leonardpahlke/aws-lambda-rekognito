from Util.Util import *
from main.config import *
from Util.UtilDynamoDB import get_results

'''
Services: DynamoDB
return results for user image
'''


class GetImageResult(MethodAction):
    def set_method(self):
        self.http_method = GET
        self.option = 'image-results'

    def execute(self, message):
        # username_key which can be translated into the s3_object_key
        # TODO message['message']
        message = message['message']

        # check if message parameter are set
        if 'user' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[GetImageResult] parameter user not set')
        username = message['user']

        result = get_results(username)
        return set_response(
            self.response,
            log='[GetImageResult] result found'.format(username),
            message='Results retrieved',
            data=result
        )
