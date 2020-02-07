from Util.Util import *
from Util.UtilDynamoDB import store_results_in_dynamo_db
from Util.UtilRekognition import compare_image_similarity, image_person_count
from Util.UtilS3 import give_me_celeb_picture_keys, upload_image

'''
execute the celeb-identifier and get a celebrity match to your uploaded user-image 
Services: S3, DynamoDB, Recognition
Flowchart:
    1. compare U-image to all celeb-images and take image reference of highest match 
    2. store U-image to s3
    3. store results to DB
return if celebrity image upload succeeded
'''


class PostUserImage(MethodAction):
    image = ''
    name = ''

    def set_method(self):
        self.http_method = POST
        self.option = 'user-image'

    def execute(self, message):
        # TODO message['message']
        message = message['message']

        # check if message parameter are set
        if 'request' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[PostUserImage] parameter request not set')
        if 'user' not in message:
            self.response = DEFAULT_BAD_RESPONSE
            return set_response(self.response, log='[PostUserImage] parameter user not set')
        # TODO get image data from message
        #  self.image = message['request']
        self.image = b64_test_image()
        self.name = message['user']

        # store user image in s3
        s3_user_key = upload_image(self.name, USER_FOLDER, self.image)

        # count persons in picture
        identified_persons = image_person_count(self.image)
        if identified_persons > 1:
            # return bad request if more than one person is found in the picture
            return set_response(
                self.response,
                message='Too many persons identified',
                data={'success': False},
                log='[PostUserImage] {} persons identified; only one is allowed'.format(identified_persons)
            )

        # get celeb images
        generator_celeb_images = give_me_celeb_picture_keys()
        best_similarity = 0.
        celeb_match = ''
        for celeb_s3_key in generator_celeb_images:
            # compare user image with celeb image
            similarity_temp = compare_image_similarity(
                IMAGE_SOURCE_BUCKET, s3_user_key,
                IMAGE_SOURCE_BUCKET, celeb_s3_key
            )
            if similarity_temp > best_similarity:
                # update best match image
                best_similarity = similarity_temp
                celeb_match = celeb_s3_key
        # store results in dynamo DB
        store_results_in_dynamo_db(s3_user_key, celeb_match, best_similarity)
        celeb_name = get_name_from_s3_key(celeb_match)
        return set_response(
            self.response,
            message="Success! you are {} similar to {}".format(best_similarity, celeb_name),
            log="[PostUserImage] image match {} with {}".format(best_similarity, celeb_name),
            data={'celebrity': celeb_name, 'confidence': best_similarity, 'success': True}
        )
