# -*- coding: utf-8 -*-

import os
import base64
import bottle
import random
import json
import subprocess
from wand.image import Image


# 随机字符串
def randomStr(num=5): return "".join(
    random.sample('abcdefghijklmnopqrstuvwxyz', num))


@bottle.route('/compress', method='POST')
def compress():
    try:
        # 接收文件
        post_data = json.loads(bottle.request.body.read().decode("utf-8"))
        image = post_data.get("image", None)
        quality = int(post_data.get("quality", 75))
        format = post_data.get("format", "jpg")
        image = image.split("base64,")[1]
        image_path = "/tmp/{}.{}".format(randomStr(10), format)
        new_image_path = "/tmp/{}-out.{}".format(randomStr(10), format)

        # 图片获取
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(image))

        # 获取图片大小
        size = os.path.getsize(image_path)

        with Image(filename=image_path) as img:
            img.compression_quality = quality
            img.save(filename=new_image_path)

        with open(new_image_path, 'rb') as f:
            base64_data = base64.b64encode(f.read()).decode("utf-8")

        # 获取新图片大小
        new_size = os.path.getsize(new_image_path)

        temp_response = {
            "source": {
                "picture": image,
                "size": size
            },
            "compress": {
                "picture": base64_data,
                "size": new_size
            }
        }
        # clean
        os.remove(image_path)
        os.remove(new_image_path)

        return temp_response
    except Exception as e:
        return "Error: %s" % (temp_response)


@ bottle.route('/', method='GET')
def index():
    return bottle.template('./index.html')


app = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=8080)
