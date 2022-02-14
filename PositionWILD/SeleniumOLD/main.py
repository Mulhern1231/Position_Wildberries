#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

from multiprocessing import Pool


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


def searchProduct(request, artic):
    status = False
    s1 = datetime.now()
    for pageNumber in range(1,1000):
        driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?page={pageNumber}&search={str(request)}")
        while True:
            try:
                if driver.find_element(By.CLASS_NAME, 'product-card-overflow'):
                    list = driver.find_elements(By.CLASS_NAME, 'product-card')
                    break
            except:
                pass

        for i in list:
            if i.get_attribute('data-popup-nm-id') == str(artic):
                s = str( str(int(i.get_attribute('data-card-index')) + 1) + ' - Место ' + str(pageNumber) + ' - Страница ')
                status = True
                break

        if status:
            break
        #li.append(str(datetime.now() - start_time))
    print(s, 'Общее время работы на товар -', datetime.now() - s1, "Артикл:", artic)



if __name__ == "__main__":
    with Pool() as pool:
        s1 = datetime.now()
        # pool.starmap(searchProduct, [('платье', 9477175), ('платье', 44300254), ('платье', 36177653),  ('платье', 29683323)])
        # pool.close()
        # pool.join()
        searchProduct('платье', 9477175)
        driver.quit()
        print(datetime.now() - s1)