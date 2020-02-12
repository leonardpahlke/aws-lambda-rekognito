from Util.Util import *
from main.config import *
from Util.UtilDynamoDB import does_celeb_exist

'''
Services: DynamoDB
return a stored celebrity
'''


class GetCelebrityNames(MethodAction):
    def set_method(self):
        self.http_method = 'GET'
        self.option = 'celebrity-names'

    def execute(self, message):
        # TODO message['message']
        message = message['message']

        # check if message parameter are set
        if 'request' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[GetCelebrityNames] parameter request not set')
        celeb_requested = message['request']
        if celeb_requested == 'ALL':
            # return all celebrities
            pass
        else:
            # return is requested celebrity in system
            response = does_celeb_exist(celeb_requested)
            if response != {}:
                return set_response(self.response,
                                    message='Celebrity {} found'.format(celeb_requested),
                                    log='[GetCelebrityNames] celeb {} found'.format(celeb_requested),
                                    data=response)
            else:
                return set_response(self.response,
                                    message='Celebrity {} not found'.format(celeb_requested),
                                    log='[GetCelebrityNames] celeb {} not found'.format(celeb_requested),
                                    data=response)
