# from importlib.resources import contents
from pip import main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from time import sleep
import json 
def initDriver():
    CHROMEDRIVER_PATH = 'chromedriver'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver

def checkLiveClone(driver):
    try:
        driver.get("https://touch.facebook.com/")
        sleep(2)
        driver.get("https://touch.facebook.com/")
        sleep(1)
        elementLive = driver.find_elements_by_xpath('//a[contains(@href, "/messages/")]')
        if (len(elementLive) > 0):
            print("Live")
            return True

        return False
    except:
        print("Check Live Fail")


def convertToCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except:
        print("Error Convert Cookie")


def checkLiveCookie(driver, cookie):
    try:
        driver.get('https://touch.facebook.com/')
        sleep(1)
        driver.get('https://touch.facebook.com/')
        sleep(2)
        loginFacebookByCookie(driver ,cookie)

        return checkLiveClone(driver)
    except:
        print("check live fail")


def loginFacebookByCookie(driver ,cookie):
    try:
        cookie = convertToCookie(cookie)
        print(cookie)
        if (cookie != None):
            script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
            driver.execute_script(script)
            sleep(5)
    except:
        print("loi login")

def outCookie(driver):
    try:
        sleep(1)
        script = "javascript:void(function(){ function deleteAllCookiesFromCurrentDomain() { var cookies = document.cookie.split(\"; \"); for (var c = 0; c < cookies.length; c++) { var d = window.location.hostname.split(\".\"); while (d.length > 0) { var cookieBase = encodeURIComponent(cookies[c].split(\";\")[0].split(\"=\")[0]) + '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path='; var p = location.pathname.split('/'); document.cookie = cookieBase + '/'; while (p.length > 0) { document.cookie = cookieBase + p.join('/'); p.pop(); }; d.shift(); } } } deleteAllCookiesFromCurrentDomain(); location.href = 'https://mbasic.facebook.com'; })();"
        driver.execute_script(script)
    except:
        print("loi login")

def getCmt(parent):
    try:
        infoCmt = {}
        mainPart = parent.find_element_by_xpath('./div/div[@class="_2b06"] | ./div[@class="_2b06"]')
        owner = mainPart.find_element_by_xpath('./div[@class="_2b05"]').text
        infoCmt['Owner']=owner
        url_owner = mainPart.find_element_by_xpath('./div[@class="_2b05"]/a').get_attribute('href')
        infoCmt['URL Owner']=url_owner
        text = mainPart.find_element_by_xpath('./div[not(@class="_2b05")]').text
        infoCmt['Cmt'] = text
        replyCmt = parent.find_elements_by_xpath('./div[@class="_2a_m"]/div/div[@class="_2a_i"]/div[@class="_2b04"]')
        infoCmt['Number reply'] = len(replyCmt)
        if len(replyCmt)>0:
            print(f"Comment của {owner} này có {len(replyCmt)} reply")
            print("Đang lấy reply...")
            listReply = []
            for r in replyCmt:
                listReply.append(getCmt(r))
            infoCmt["Reply cmt"] = listReply
            print("Đã lấy xong reply :)")
        return infoCmt
    except:
        pass


def getPoster(driver,postId):
    try:
        print(f"Đang lấy thông tin của post có ID là {postId}")
        infoPost={}
        infoPost['URL post'] = "https://touch.facebook.com/" + str(postId)
        driver.get("https://touch.facebook.com/" + str(postId))
        try:
            contentPosts = driver.find_element_by_xpath('//*[@class="_5rgt _5nk5"]/div | //*[@class="msg"]/div')
        except:
            return None
        # print(contentPosts.text)
        infoPost["Content"] = contentPosts.text
        viewMoreReply = driver.find_elements_by_xpath('//*[@class="_2b1h async_elem"]/a')
        for x in viewMoreReply:
            try:
                x.click()
            except:
                continue
        listCmt=[]
        for i in range(10):
            try:
              viewMoreCmt = driver.find_element_by_xpath('//div[@class="async_elem"]')
              sleep(2)
              viewMoreCmt.click()
              sleep(3)
            except:
              break
        comments = driver.find_elements_by_xpath('.//div[@class="_333v _45kb"]/div[contains(@class,"_2a_i")]/div[@class="_2b04"]')
        print(len(comments))
        if len(comments)==0 or len(contentPosts.text)==0:
          print("Post này ko có comment :(")
          return None
        for comment in comments:
          listCmt.append(getCmt(comment))
        infoPost['Comment'] = listCmt
        return infoPost
    except Exception as e:
        print("getPoster Failed")
        print(e)
def Scroll(driver,Max):
    last_height = driver.execute_script("return document.body.scrollHeight")
    numScroll = 0
    while numScroll <= Max:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        numScroll+=1
def getPostIds(driver):
    allPostIds = []
    Scroll(driver,5)
    sleep(2)
    shareBtn = driver.find_elements_by_xpath('//a[contains(@href, "/sharer.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0]
            if postId not in allPostIds:
                # print(postId)
                allPostIds.append(postId)
    return allPostIds

def getnumOfPost(driver, pageId):
    driver.get("https://touch.facebook.com/" + pageId)
    return getPostIds(driver)