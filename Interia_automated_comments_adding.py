import requests
from selenium import webdriver
from lxml.html import fromstring
import lxml as lxml
import pandas as pd
from openpyxl import load_workbook
from time import sleep
import itertools
from itertools import cycle


browser = 0
button3 = 0
url = 'https://httpbin.org/ip'
url2 = 'https://sport.interia.pl/skoki-narciarskie/news-ps-w-skokach-zyla-i-stoch-na-podium-kobayashi-najlepszy-w-en,nId,2734417'
komentarz_poczatkowy = 1
komentarz_ostatni = 6
krok = 2
odstep_czasowy = 0.5
sekundy = odstep_czasowy*60
p = komentarz_poczatkowy-1

wb = load_workbook('./arkusz_interia.xlsx')
sheet = wb['Arkusz1']
df = pd.DataFrame(sheet.values)
data = sheet.values
data = list(data)
print(data)

ww = pd.read_excel('arkusz_interia.xlsx', sheet_name='Arkusz1')
nick = ww['tytul'].tolist()
print(nick)
rozwiniecie = ww['tresc'].tolist()
print(rozwiniecie)
column3 = pd.read_excel('arkusz_interia.xlsx', usecols=[2])
print(column3)

while p < komentarz_ostatni:
    def get_proxies():
        url = 'https://free-proxy-list.net/'
        sleep(1)
        response = requests.get(url)
        sleep(1)
        parser = fromstring(response.text)
        sleep(1)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy1 = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                sleep(1)
                proxies.add(proxy1)
                sleep(1)
        return proxies

    sleep(1)
    proxies = get_proxies()
    sleep(1)
    print(proxies)
    sleep(1)
    proxy_pool = cycle(proxies)
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print(proxy)
        print("Request #%d" % i)
        try:
            x = 0
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.json())
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy)
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get(url2)
            sleep(2)
            button1 = browser.find_element_by_class_name('rodo-popup-agree')
            sleep(2)
            button1.click()
            sleep(2)
            button2 = browser.find_element_by_class_name('is-comment-container')
            sleep(2)
            button2.click()
            sleep(2)
            nik = browser.find_element_by_css_selector('.forum__add-user-author-input')
            sleep(2)
            nik.send_keys(nick[p])
            sleep(2)
            tresc = browser.find_element_by_class_name('forum__add-content-input')
            sleep(2)
            tresc.send_keys(rozwiniecie[p])
            sleep(2)
            try:
                button3 = browser.find_element_by_class_name('recommend-flybar-button-inside')
            except:
                continue
            sleep(2)
            if button3 != 0:
                button3.click()
            sleep(2)
            button4 = browser.find_element_by_css_selector('.forum--is-small .forum__add-bottom-submit')
            sleep(2)
            button4.click()
            sleep(2)
            browser.quit()
            p += krok
            break
        except:
            print("Skipping. Connnection error")
            if browser != 0:
                browser.quit()
            sleep(2)
            continue


