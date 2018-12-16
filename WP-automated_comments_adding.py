import requests
from selenium import webdriver
from lxml.html import fromstring
import lxml as lxml
import pandas as pd
from openpyxl import load_workbook
from time import sleep
import itertools
import re
from itertools import cycle



url = 'https://httpbin.org/ip'
url2 = 'https://wiadomosci.wp.pl/trudne-warunki-pogodowe-w-osmiu-wojewodztwach-ostrzezenia-gddkia-i-imgw-6328272650184833a'
komentarz_poczatkowy = 1
komentarz_ostatni = 6
krok = 2
odstep_czasowy = 0.5
sekundy = odstep_czasowy*60
p = komentarz_poczatkowy-1

wb = load_workbook('./arkusz_wp.xlsx')
sheet = wb['Arkusz1']
df = pd.DataFrame(sheet.values)
data = sheet.values
data = list(data)
print(data)

ww = pd.read_excel('arkusz_wp.xlsx', sheet_name='Arkusz1') # can also index sheet by name or fetch all sheets
nick = ww['tytul'].tolist()
print(nick)
rozwiniecie = ww['tresc'].tolist()
print(rozwiniecie)
column3 = pd.read_excel('arkusz_wp.xlsx', usecols=[2])
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
                proxies.add(proxy1)
        return proxies

    proxies = get_proxies()
    sleep(1)
    print(proxies)
    sleep(1)
    proxy_pool = itertools.cycle(proxies)
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print(proxy)
        print("Request #%d" % i)
        try:
            x = 0
            sleep(1)
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            sleep(1)
            print(response.json())
            chrome_options = webdriver.ChromeOptions()
            sleep(1)
            chrome_options.add_argument('--proxy-server=%s' % proxy)
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get(url2)
            sleep(2)
            x = browser.page_source
            sleep(2)
            y = re.search(r"(?<=ZAAWANSOWANE).*?(>PRZECHODZĘ)", x).group(0)
            sleep(2)
            print(y)
            sleep(2)
            m = re.search('class="(.+?)"', y)
            if m:
                z = m.group(1)
            sleep(2)
            print(z)
            sleep(3)
            button0 = browser.find_element_by_class_name(z)
            sleep(2)
            button0.click()
            sleep(2)
            button1 = browser.find_element_by_css_selector('.dLGbQpo')
            sleep(2)
            button1.click()
            sleep(2)
            button2 = browser.find_element_by_css_selector('._1488wuC ._3zg4UkP')
            sleep(2)
            button2.click()
            sleep(2)
            koment = browser.find_element_by_id('text')
            sleep(2)
            koment.send_keys(rozwiniecie[p])
            sleep(2)
            nik = browser.find_element_by_class_name('_3970n2q')
            sleep(2)
            nik.send_keys(nick[p])
            sleep(2)
            button3 = browser.find_element_by_class_name('_3j-DhSR')
            sleep(2)
            button3.click()
            sleep(2)
            p += krok
            break
        except:
            print("Skipping. Connnection error")
            browser.quit()
            sleep(2)
            continue