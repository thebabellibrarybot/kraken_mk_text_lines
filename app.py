import boto3
import cv2
from io import BytesIO
import numpy as np

s3 = boto3.client('s3')

"""
for prac

def show_coords(image, coords):
    for coord in coords:
        x, y, w, h = coord
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

def kraken_kropper(img, coords, bucket_name, original_name):
    s3_urls = []
    s3_keys = []
    for i, coord in enumerate(coords):
        x, y, w, h = coord
        crop = img[y:h, x:w]
        key = f"{str(i)}_{original_name}"
        _, buffer = cv2.imencode(".jpg", crop)
        #cv2.imwrite(str(i)+original_name, crop) # for local testing
        s3.upload_fileobj(BytesIO(buffer), bucket_name, key)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        s3_urls.append(s3_url)
        s3_keys.append(key)
    return s3_urls, s3_keys

def lambda_handler(event, context):
    coords = event['body']['coords']
    buk = event['body']['bucket']
    key = event['body']['key']

    img_obj = s3.get_object(Bucket=buk, Key=key)
    img_data = img_obj['Body'].read()
    img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    out = kraken_kropper(img, coords, buk, key)
    return out


"""
prac:

e = {
    "body": {
    "key":"cropped_'0'__'1'__'2'_26fe16c5-26a3-4333-b077-e181b965efbefol.146_1L.jpg",
    "bucket": "thisthatbukfornola",
    "coords": [[274, 145, 522, 162],[4, 162, 525, 175],[275, 180, 531, 197],[275, 199, 538, 216],[274, 215, 536, 233],[274, 233, 531, 251],[275, 251, 535, 268],[312, 268, 531, 286],[322, 288, 533, 304],[350, 305, 536, 330],[274, 323, 532, 358],[397, 324, 535, 342],[275, 360, 526, 377],[276, 374, 532, 395],[276, 392, 530, 411],[276, 412, 538, 426],[294, 428, 536, 446]]
    }
}
i = lambda_handler(e, context = None)
print(i)
"""