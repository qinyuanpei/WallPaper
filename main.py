#!/usr/bin/python
# -*- coding: utf-8 -*-  
import os
import re
import sys
import json
import random
import requests
from os import path
from PIL import Image
from bs4 import BeautifulSoup
import win32gui,win32con,win32api

# Query Images
searchURL = 'https://unsplash.com/napi/search?client_id=%s&query=%s&page=1'
client_id = 'fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7'
categories = ['nature','flowers','wallpaper','landscape','sky']
searchURL = searchURL % (client_id,random.choice(categories))
response = requests.get(searchURL)
print(u'正在从Unsplash上搜索图片...')

# Parse Images
print(response)
data = json.loads(response.text)
results = data['photos']['results']
print(u'已为您检索到图片共%s张' % str(len(results)))
results = list(filter(lambda x:float(x['width'])/x['height'] >=1.33,results))
result = random.choice(results)
resultId = str(result['id'])
resultURL = result['urls']['regular']

# Download Images
print(u'正在为您下载图片:%s...' % resultId)
basePath = sys.path[0]
if(os.path.isfile(basePath)):
    basePath = os.path.dirname(basePath)
baseFolder = basePath + '\\Download\\'
if(not path.exists(baseFolder)):
    os.makedirs(baseFolder)
jpgFile = baseFolder + resultId + '.jpg'
bmpFile = baseFolder + resultId + '.bmp'
response = requests.get(resultURL)
with open(jpgFile,'wb') as file:
    file.write(response.content)
img = Image.open(jpgFile)
img.save(bmpFile,'BMP')
os.remove(jpgFile)

# Update WallPaper
print(u'正在设置图片:%s为桌面壁纸...' % resultId)
key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
    "Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmpFile, 1+2)
print(u'成功应用图片:%s为桌面壁纸'  % resultId)
