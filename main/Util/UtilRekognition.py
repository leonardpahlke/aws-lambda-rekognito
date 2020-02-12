import boto3

client_rekognition = boto3.client('rekognition')


# detect if image contains an celebrity
def is_celebrity(image_bytes):
    is_celeb = False
    name, confidence = "", 0.
    response = client_rekognition.recognize_celebrities(Image={'Bytes': image_bytes})
    if 'CelebrityFaces' in response:
        celebrity_faces = response['CelebrityFaces']
        if celebrity_faces.__len__() != 0:
            celebrity_face = celebrity_faces[0]
            name = celebrity_face['Name']
            confidence = celebrity_face['MatchConfidence']
            is_celeb = True
    return is_celeb, name, confidence


# detect how many persons are identified in the image
def image_person_count(image_bytes, false_tolerance=90.):
    person_count = 0
    # TODO filter only 'Person' (not everything else as well)
    response = client_rekognition.detect_labels(Image={'Bytes': image_bytes})
    # response structure
    # "Labels": [{"Name": "Person",
    #             "Confidence": 99.64553833007812,
    #             "Instances": [...persons...]}, {...}]
    labels = list(response['Labels'])
    person_detection_information = [x for x in labels if x['Name'] == 'Person']
    if person_detection_information:
        person_count = person_detection_information[0]['Instances'].__len__()
        if person_count > 1:
            person_count = 0
            for person_detected in person_detection_information[0]['Instances']:
                # check if person detection confidence is over false_tolerance
                # system can false identify persons in a picture percentage
                # don't interpret person as a person if system isn't sure 90. percent <- false_tolerance
                if person_detected['Confidence'] > false_tolerance:
                    person_count += 1
    return person_count


# return how similar two images are
def compare_image_similarity(bucket_source, key_source, bucket_target, key_target, threshold=0.):
    # compare two faces recognized in the image
    response = client_rekognition.compare_faces(
        SourceImage={"S3Object": {"Bucket": bucket_source, "Name": key_source}},
        TargetImage={"S3Object": {"Bucket": bucket_target, "Name": key_target}},
        SimilarityThreshold=threshold,
    )
    return response['FaceMatches'][0]['Similarity']
