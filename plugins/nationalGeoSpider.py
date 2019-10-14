import os
import re
import sys
import uuid
import json
import random
import requests
from os import path
from bs4 import BeautifulSoup

# 国家地理壁纸插件
class NationalGeoSpider:

    def getImage(self,downloadFolder): 
        url = 'https://www.nationalgeographic.com/photography/photo-of-the-day/_jcr_content/.gallery.json' 
        response = requests.get(url) 
        # print(response.text)
        data = json.loads(response.text)
        imgs = data['items']
        length = len(imgs)
        if length > 0:
            match = random.choice(imgs)
            rawUrl = match['originalUrl']
            rawId = str(uuid.uuid1())
            raw = requests.get(rawUrl) 
            imgFile = os.path.join(downloadFolder, rawId)
            with open(imgFile,'wb') as f:
                f.write(raw.content)
        return imgFile