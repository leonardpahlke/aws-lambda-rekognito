from Util.Util import *
from main.config import *
from Util.UtilDynamoDB import does_celeb_exist, store_new_celeb
from Util.UtilRekognition import image_person_count, is_celebrity
from Util.UtilS3 import update_celeb_image, upload_image

'''
upload Celebrity images to aws
Services: S3, DynamoDB, Recognition
Flowchart:
    1. check if image contains a celebrity
    2. check if celebrity isn't already in DB
    3. reduce image resolution
    4. store image in s3 bucket and  celebrity-name in DB
return submission status
'''


class PostCelebrityImage(MethodAction):
    image = ''

    def set_method(self):
        self.http_method = 'POST'
        self.option = 'celebrity-image'

    def execute(self, message):
        # TODO message['message']
        message = message['message']

        # check if message parameter are set
        if 'request' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[PostCelebrityImage] parameter request not set')
        # TODO get image data from message
        #  self.image = message['request']
        self.image = b64_test_image()

        # count persons in picture
        identified_persons = image_person_count(self.image)
        if identified_persons > 1:
            # return bad request if more than one person is found in the picture
            return set_response(
                self.response,
                message='Too many persons identified',
                data={'celebrity': False},
                log='[PostCelebrityImage] {} persons identified; only one is allowed'.format(identified_persons)
            )

        # get celebrity data if identified
        is_celeb, new_celeb_image_name, new_celeb_image_confidence = is_celebrity(self.image)
        if not is_celeb:
            # return bad request if image doesn't contain a celebrity
            return set_response(
                self.response,
                message='image doesnt contain a celebrity',
                data={'celebrity': False},
                log='[PostCelebrityImage] didnt identified a celebrity'
            )

        # check if detected celebrity is already in system
        response_celeb_db = does_celeb_exist(new_celeb_image_name)
        # celeb exist in DB
        if response_celeb_db != {}:
            if new_celeb_image_confidence > response_celeb_db['confidence']:
                # update image with new posted image
                update_celeb_image(new_celeb_image_name, self.image)
                return set_response(
                    self.response,
                    message='We got {} already in our System and the picture doesnt seem to be better'
                        .format(new_celeb_image_name),
                    log='[PostCelebrityImage] submitted celeb: {} is already in system and din\'t got updated'
                        .format(new_celeb_image_name)
                )
        else:
            # upload image to s3
            key = upload_image(new_celeb_image_name, CELEBRITIES_FOLDER, self.image)
            # store celeb in dynamo db
            store_new_celeb(key, new_celeb_image_confidence, new_celeb_image_name)
        return set_response(
            self.response,
            message='{} registered'.format(new_celeb_image_name),
            log='[PostCelebrityImage] added celebrity to System'.format(new_celeb_image_name),
            data={'celebrity': False, 'confidence': new_celeb_image_confidence}
        )
