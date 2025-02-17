# from importlib.resources import contents
from this import d
from pip import main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from time import sleep, time
from dotenv import load_dotenv


def timer(func):
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        print('=> Loading time:', end - start)
    return wrapper


load_dotenv()

# USERNAME = os.getenv('USERNAME_FACEBOOK')
# PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAME_FACEBOOK')
PASSWORD = '0147258369'

modeScroll = "INFINITY"
maxScroll = 50
sleepTime = 2
maxViewMore = 20


def initDriver(headless=True, usingProfile=False):
    CHROMEDRIVER_PATH = 'chromedriver'
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    if usingProfile:
        # print(f"--user-data-dir={os.getenv('USER_DATA_PATH')}")
        chrome_options.add_argument(
            f"--user-data-dir={os.getenv('USER_DATA_PATH')}")
        chrome_options.add_argument(
            f"--profile-directory={os.getenv('PROFILE_NAME')}")
    # chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument(
        '--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument(
        "--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControllered")
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # open Browser in maximized mode
    chrome_options.add_argument("--start-maximized")
    # overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2})

    # # Incognito
    # # chrome_options.add_argument('--incognito')
    # chrome_options.add_argument(
    #     '--disable-blink-features=AutomationControlled')

    # chrome_options.add_experimental_option('prefs', {
    #     'profile.managed_default_content_settings.images': 2,
    #     'profile.managed_default_content_settings.stylesheets': 2,
    #     'profile.managed_default_content_settings.cookies': 2,
    #     'profile.managed_default_content_settings.geolocation': 2,
    #     'profile.managed_default_content_settings.media_stream': 2,
    #     'profile.managed_default_content_settings.plugins': 1,
    #     'profile.default_content_setting_values.notifications': 2,
    # })

    driver = webdriver.Chrome(CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver


def loadExtensionVPN(driver):
    driver.get(
        "chrome-extension://bihmplhobchoageeokmgbdihknkjbknd//panel//index.html")
    sleep(3)
    connectButton = driver.find_element_by_css_selector("#ConnectionButton")
    if "Stop" not in connectButton.text:
        connectButton.click()
    return driver


def loginFacebook(driver):
    driver.get("https://touch.facebook.com/")
    sleep(sleepTime)
    usernameInput = driver.find_element_by_css_selector(
        '._56bg._4u9z._5ruq._8qtn')
    print(USERNAME)
    usernameInput.send_keys(USERNAME)
    passwordInput = driver.find_element_by_css_selector(
        '._56bg._4u9z._27z2._8qtm')
    passwordInput.send_keys(PASSWORD)

    buttonLogin = driver.find_element_by_css_selector(
        '._54k8._52jh._56bs._56b_._28lf._9cow._56bw._56bu')
    buttonLogin.click()
    return driver


def checkLiveClone(driver):
    try:
        driver.get("https://touch.facebook.com/")
        sleep(sleepTime)
        driver.get("https://touch.facebook.com/")
        sleep(1)
        elementLive = driver.find_elements_by_xpath(
            '//a[contains(@href, "/messages/")]')
        if (len(elementLive) > 0):
            print("Live")
            return True

        return False
    except BaseException:
        print("Check Live Fail")


def convertToCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + \
                    (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + \
                    (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except BaseException:
        print("Error Convert Cookie")


def checkLiveCookie(driver, cookie):
    try:
        driver.get('https://touch.facebook.com/')
        sleep(1)
        driver.get('https://touch.facebook.com/')
        sleep(sleepTime)
        loginFacebookByCookie(driver, cookie)

        return checkLiveClone(driver)
    except BaseException:
        print("check live fail")


def loginFacebookByCookie(driver, cookie):
    try:
        cookie = convertToCookie(cookie)
        print(cookie)
        if (cookie is not None):
            script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
            driver.execute_script(script)
            sleep(5)
    except BaseException:
        print("loi login")


def outCookie(driver):
    try:
        sleep(1)
        script = "javascript:void(function(){ function deleteAllCookiesFromCurrentDomain() { var cookies = document.cookie.split(\"; \"); for (var c = 0; c < cookies.length; c++) { var d = window.location.hostname.split(\".\"); while (d.length > 0) { var cookieBase = encodeURIComponent(cookies[c].split(\";\")[0].split(\"=\")[0]) + '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path='; var p = location.pathname.split('/'); document.cookie = cookieBase + '/'; while (p.length > 0) { document.cookie = cookieBase + p.join('/'); p.pop(); }; d.shift(); } } } deleteAllCookiesFromCurrentDomain(); location.href = 'https://mbasic.facebook.com'; })();"
        driver.execute_script(script)
    except BaseException:
        print("loi login")


# @timer
def getCmt(parent):
    try:
        infoCmt = {}
        try:
            owner = parent.find_element_by_css_selector("._2b05").text
            infoCmt['Owner'] = owner
        except Exception as e:
            print(e)

        # url_owner = mainPart.find_element_by_xpath(
        #     './div[@class="_2b05"]/a').get_attribute('href')
        # infoCmt['URL Owner'] = url_owner
        text = parent.find_element_by_css_selector(
            '[data-sigil="comment-body"]').text
        infoCmt['Cmt'] = text

        replyCmt = parent.find_elements_by_css_selector('._2a_m ._2a_i ._2b04')
        infoCmt['Number reply'] = len(replyCmt)
        if len(replyCmt) > 0:
            print(f"Comment của {owner} này có {len(replyCmt)} reply")
            print("Đang lấy reply...")
            listReply = []
            for r in replyCmt:
                listReply.append(getCmt(r))
            infoCmt["Reply cmt"] = listReply
            print("Đã lấy xong reply :)")
        return infoCmt
    except Exception as e:
        print(e)


# @timer
def getPoster(driver, postId):
    try:
        print(f"Đang lấy thông tin của post có ID là {postId}")
        infoPost = {}
        infoPost['URL post'] = "https://touch.facebook.com/" + str(postId)
        driver.get("https://touch.facebook.com/" + str(postId))

        contentPosts = ""
        try:
            contentPosts = driver.find_element_by_css_selector(
                '._5rgt._5nk5')
        except Exception as e:
            print(e)

        try:
            media = driver.find_element_by_css_selector('._5rgu._7dc9._27x0')
            infoPost['Has media'] = True
            Images = media.find_elements_by_css_selector('a')
            if len(Images) > 0:
                infoPost['Media'] = []
                for image in Images:
                    infoPost['Media'].append(image.get_attribute('href'))
        except Exception as e:
            infoPost['Has media'] = False
            print("Post không có media")

        # Get time
        # time = driver.find_element_by_css_selector(
        #     '._5rgr.async_like')
        # jsonTime = time.get_attribute(
        #     "data-ft").split('publish_time":')[1].split(',')[0]
        # infoPost['Timestamp'] = jsonTime

        # print(contentPosts.text)

        # Click view more button
        numViewMore = 0
        try:
            last_height = driver.execute_script(
                "return document.body.scrollHeight")

            while True:
                numViewMore += 1
                viewMoreButton = driver.find_element_by_css_selector("._108_")
                if viewMoreButton is None or numViewMore > maxViewMore:
                    break
                viewMoreButton.click()

                print(f"Click view more button {numViewMore} time")
                sleep(3)

                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    break

                last_height = new_height

        except Exception as e:
            print("Không có bình luận cần tải thêm")

        infoPost["Content"] = contentPosts.text
        # Get text of comment

        try:
            numViewMoreReply = 0
            while True:
                numViewMoreReply += 1
                if numViewMoreReply > 10:
                    break
                viewMoreReply = driver.find_elements_by_css_selector(
                    '[data-sigil="replies-see-more"]')
                if viewMoreReply is None or len(viewMoreReply) == 0:
                    break
                for x in viewMoreReply:
                    try:
                        # print(x.text)
                        x.click()
                    except Exception as e:
                        pass
                        # print(e)
                print(f"Click view more reply {len(viewMoreReply)} element")
                sleep(4)
        except Exception as e:
            print(e)

        listCmt = []

        comments = driver.find_elements_by_css_selector(
            "div._2a_i[data-sigil='comment']")
        print(len(comments))
        if len(comments) == 0 or len(contentPosts.text) == 0:
            print("Post này ko có comment :(")
            return None
        for comment in comments:
            listCmt.append(getCmt(comment))
        infoPost['Comment'] = listCmt
        # print(infoPost)

        return infoPost
    except Exception as e:
        print("getPoster Failed")
        print(e)


def Scroll(driver, maxScroll):
    last_height = driver.execute_script("return document.body.scrollHeight")
    numScroll = 0
    while True:
        try:
            closeLoginButton = driver.find_element_by_css_selector("._4b-n")
            closeLoginButton.click()
        except Exception as e:
            pass

        try:
            viewMorePost = driver.find_element_by_css_selector(
                '.title.mfsm.fcl')
            viewMorePost.click()
        except Exception as e:
            print("Không tim thấy nút 'xem thêm post'")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        print(f"Srolling {numScroll} time")
        sleep(sleepTime)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if modeScroll == "INFINITY":
            if new_height == last_height and numScroll > maxScroll:
                break
        elif numScroll >= maxScroll:
            break
        last_height = new_height
        numScroll += 1


def getPostIds(driver, type="PAGE"):
    allPostIds = []
    Scroll(driver, maxScroll)
    sleep(sleepTime)
    if type == "GROUP":
        post = driver.find_elements_by_xpath(
            '//a[contains(@href, "/sharer.php")]')
    else:
        post = driver.find_elements_by_css_selector('article')
    if (len(post)):
        for link in post:

            if type == "GROUP":
                postId = link.get_attribute('href').split('sid=')[
                    1].split('&')[0]
            else:
                print(link.get_attribute('data-store').split('post_id')
                      [-1].split(',')[0].split(':')[-1])
                postId = link.get_attribute(
                    'data-store').split('post_id')[-1].split(',')[0].split(':')[-1]
            if postId not in allPostIds:
                # print(postId)
                allPostIds.append(postId)
    return allPostIds


def getnumOfPost(driver, pageId):
    driver.get("https://touch.facebook.com/" + pageId)
    if "groups" in pageId:
        return getPostIds(driver, "GROUP")
    return getPostIds(driver, "PAGE")
