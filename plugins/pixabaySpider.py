import os
import re
import sys
import uuid
import json
import random
import requests
from os import path
from bs4 import BeautifulSoup

# Pixabay
class PixabaySpider:

    def getImage(self, downloadFolder): 
        
        url = 'http://pixabay.com/api/?key=30271602-41319186b7198e7712c568e90&lang=zh&editors_choice=true' 
        response = requests.get(url) 
        response = json.loads(response.text)
        imgs = response['hits']
        length = len(imgs)
        if length > 0:
            match = random.choice(imgs)
            rawUrl = match['largeImageURL']
            rawId = rawUrl.split('/')[-1]
            raw = requests.get(rawUrl) 
            imgFile = os.path.join(downloadFolder, rawId)
            with open(imgFile,'wb') as f:
                f.write(raw.content)
        return imgFile