# -*- coding: utf-8 -*-

import oss2
import json
import os
from wand.image import Image


def handler(event, context):
    evt = json.loads(event)
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id,
                        creds.access_key_secret, creds.security_token)
    endpoint = "oss-{}-internal.aliyuncs.com".format(context.region)
    if evt.get('region') and evt.get('region') != context.region:
        endpoint = "oss-{}.aliyuncs.com".format(evt.get('region'))
    bucketName = evt.get('bucket')
    bucket = oss2.Bucket(auth, endpoint, bucketName)
    image = evt['image']
    (_, filename) = os.path.split(image)
    image_path = '/tmp/{}'.format(filename)
    new_image_path = '/tmp/new_{}'.format(filename)
    bucket.get_object_to_file(image, image_path)
    quality = evt['quality']
    with Image(filename=image_path) as img:
        img.compression_quality = quality
        img.save(filename=new_image_path)
    dst = evt['dst']
    bucket.put_object_from_file(os.path.join(dst, filename), new_image_path)
