# -*- coding: utf-8 -*-

import os
import base64
import bottle
import random
import json

# 随机字符串
randomStr = lambda num=5: "".join(random.sample('abcdefghijklmnopqrstuvwxyz', num))


@bottle.route('/compress', method='POST')
def compress():
    try:
        # 接收文件
        post_data = json.loads(bottle.request.body.read().decode("utf-8"))
        image = post_data.get("image", None)
        min_quality = post_data.get("min_quality", 65)
        max_quality = post_data.get("max_quality", 80)
        speed = post_data.get("speed", 3)

        image = image.split("base64,")[1]

        # 图片获取
        image_path = "/tmp/%s.png" % randomStr(10)
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(image))

        # 获取图片大小
        size = os.path.getsize(image_path)

        # 压缩图片
        temp_command = './pngquant --quality %s-%s --speed %s %s' % (min_quality, max_quality, speed, image_path)
        print("command: ", temp_command)
        os.system(temp_command)
        new_image_path = image_path.replace(".png", '-fs8.png')
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

        return temp_response
    except Exception as e:
        return "Error: %s"%(temp_response)

@bottle.route('/', method='GET')
def index():
    return bottle.template('./index.html')


app = bottle.default_app()
if __name__ == "__main__":
    bottle.run(host='localhost', port=8080)
