from Util.Util import *
from Util.UtilDynamoDB import does_celeb_exist

'''
Services: DynamoDB
return all stored celebrity names
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
        requested_person = message['request']

        # return is requested celebrity in system
        response = does_celeb_exist(requested_person)
        if response != {}:
            return set_response(self.response,
                                message='Celebrity {} found'.format(requested_person),
                                log='[GetCelebrityNames] celeb {} found'.format(requested_person),
                                data=response)
        else:
            return set_response(self.response,
                                message='Celebrity {} not found'.format(requested_person),
                                log='[GetCelebrityNames] celeb {} not found'.format(requested_person),
                                data=response)
