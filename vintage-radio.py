# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:28:34 2020

@author: Diogo
"""
import requests
import re
import time

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

num = 0
for id_ in range(10000):
    path = r"C:\Users\Diogo\Downloads\new\\"
    url = "https://www.vintage-radio.info/download.php?id=" + str(id_)
    
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    if filename == None:
        continue
    open(path + "id-"+str(id_) +"_" + filename, 'wb').write(r.content)
    print("id-"+str(id_) +"_" + filename)
    num = num+1
    if num == 5:
        time.sleep(35*60)
        num = 0
        