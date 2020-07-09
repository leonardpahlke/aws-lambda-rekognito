from main.Util.Util import *

# all actions that can be requests
# from Get.GetCelebrityNames import GetCelebrityNames
# from Get.GetImageResult import GetImageResult
# from Get.GetSourceImage import GetSourceImage
# from Post.PostCelebrityImage import PostCelebrityImage
# from Post.PostUserImage import PostUserImage
from main.Util.UtilRDS import *

# method_actions = [GetSourceImage(), GetImageResult(), GetCelebrityNames(),
        #          PostUserImage(), PostCelebrityImage()]


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

    # RDSDatabase().run_query(CREATE_TABLE_QUERY)

    return ''  # lambda_response
