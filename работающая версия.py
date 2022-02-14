from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

import requests
import json
from bs4 import BeautifulSoup
import ast

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=OFF')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--no-sandbox")

prefs = {'profile.default_content_setting_values': {'cookies': 0, 'images': 0, 'javascript': 0,
                            'plugins': 0, 'popups': 0, 'geolocation': 0,
                            'notifications': 0, 'auto_select_certificate': 0, 'fullscreen': 0,
                            'mouselock': 0, 'mixed_script': 0, 'media_stream': 0,
                            'media_stream_mic': 0, 'media_stream_camera': 0, 'protocol_handlers': 0,
                            'ppapi_broker': 0, 'automatic_downloads': 0, 'midi_sysex': 0,
                            'push_messaging': 0, 'ssl_cert_decisions': 0, 'metro_switch_to_desktop': 0,
                            'protected_media_identifier': 0, 'app_banner': 0, 'site_engagement': 0,
                            'durable_storage': 0}}

chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


articl = "25665520"
req = "шорты"



driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={req}')
time.sleep(3)
test = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

for item in test:
    if ("https://wbxcatalog-ru.wildberries.ru" in item["name"]) and ("catalog" in item["name"]):
        url = item["name"]
        break

status = False
for PageNum in range(1,50):
    s1 = time.time()
    URL_LIST = url.split('&')
    for i in URL_LIST:
        if "page" in i:
            numberInList = URL_LIST.index(str(i))
            URL_LIST[numberInList] = f"&page={PageNum}&"

    url = '&'.join(URL_LIST)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    d = json.loads(str(soup))

    for i in d["data"]["products"]:
        if str(articl) == str(i["id"]):
            print(PageNum)
            status = True
            break
    if status == True:
        break
    print("--- %s seconds ---" % (time.time() - s1))
