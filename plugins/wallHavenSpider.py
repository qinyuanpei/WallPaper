import os
import re
import sys
import uuid
import json
import random
import requests
from os import path

class WallHavenSpider:

    def getImage(self,downloadFolder): 
        url = 'https://alpha.wallhaven.cc/wallpaper/' 
        pattern = r'/small.+?(jpg|png)' 
        response = requests.get(url) 
        print(response.text)
        mattch = re.search(pattern, response.text) 
        imgFile = ''
        if mattch: 
            rawUrl = 'https://th.wallhaven.cc' + mattch.group(0)
            rawUrl = rawUrl.replace('https://th.wallhaven.cc/small','https://w.wallhaven.cc/full')
            rawId = rawUrl.split('/')[-1]
            rawUrl = rawUrl.replace(rawId, 'wallhaven-' + rawId)
            raw = requests.get(rawUrl) 
            imgFile = os.path.join(downloadFolder, rawId)
            with open(imgFile,'wb') as f:
                f.write(raw.content)
        return imgFile
