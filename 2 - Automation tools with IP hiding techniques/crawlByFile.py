from test import *
# from importlib.resources import contents
# from pip import main
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from time import sleep
import json
import numpy as np
import pandas as pd

# list file post
import glob
groupPost = glob.glob("data/*/*/*.json")
pagePost = glob.glob("data/*/*.json")
groupPagePost = groupPost + pagePost
listPostFile = []
for postFile in groupPagePost:
    listPostFile.append(postFile.split("\\")[-1].split(".")[0])

cookie = 'cookie: datr=zCl1YfSOcGf17m9dXXY7eSaB; sb=zg8HYr27z2Eze4zpOblULwod; dpr=1.25; locale=vi_VN; wd=1488x754; c_user=100078509210570; xs=2%3AdK7lsdMi8XwFoQ%3A2%3A1646105133%3A-1%3A-1; fr=0MRspGNSQYfr6Brep.AWWETuMAYWgC08UmlQDDNmoo6UM.BiHNcs.jK.AAA.0.0.BiHZJM.AWXjlK0yd7A; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1646105170400%2C%22v%22%3A1%7D'
driver = initDriver()
# driver.get('https://touch.facebook.com/')

namePage = [
    'groups/364997627165697',
    'nhung.truyen.ngan.hay',
    'danphunhuantphcm',
    'nhatky',
    'vntravel',
    'rapphim',
    'KHTNCFS',
    'CodeLearnFanpage',
    'pagenaykhonghetrend',
    'chuyencuaem.page'
]

# sleep(2)
driver = loginFacebook(driver)
# loginFacebookByCookie(driver ,cookie)
sleep(4)
print("start crawl")
for page in namePage:
    try:
        dsPost = {}
        Id_List = getnumOfPost(driver, page)
        if not os.path.exists(f'data/{page}'):
            os.makedirs(f'data/{page}')
        for idPost in Id_List:
            if (idPost in listPostFile):
                continue
            DS = getPoster(driver, idPost)
            if DS is not None:
                with open(f'data/{page}/{idPost}.json', "w", encoding="utf-8") as outfile:
                    json.dump(DS, outfile, ensure_ascii=False)
            # dsPost[str(idPost)]= DS
        print('Success')
    except Exception as e:
        print('Failed')
        print(e)
driver.close()
