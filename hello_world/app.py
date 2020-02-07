# method-action logic
from Get.GetImageResult import *
from Get.GetSourceImage import *
from Post.PostUserImage import *
from Get.GetCelebrityNames import *
from Post.PostCelebrityImage import *
import io

# all actions that can be requests
method_actions = [GetSourceImage(), GetImageResult(), GetCelebrityNames(),
                  PostUserImage(), PostCelebrityImage()]


def lambda_handler(event, context):
    lambda_response = DEFAULT_BAD_RESPONSE

    try:
        # get information from request
        request_method = event[METHOD]
        request_option = event[QUERY_STRING_PARAMS][OPTION]
        request_message = event[QUERY_STRING_PARAMS][MESSAGE]

        # find the requested method-action
        for method_action in method_actions:
            if (request_method == method_action.http_method) and (request_option == method_action.option):
                # execute method-action
                lambda_response = method_action.execute(request_message)
                break
    except Exception as e:
        lambda_response[BODY][LOG] = e

    return lambda_response

# print(PostUserImage().execute(
#     {"message": {
#         "user": "",
#         "request": "",
#         "celebrity": ""
#     }}
# ))


def resize_test():
    img = b64_test_image()
    resize_image(img)


resize_test()
