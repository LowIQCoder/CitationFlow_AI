import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
from secret import api_key, cheksum, chromedriver_path, chrome_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

def create_browser(webdriver_path):
    browser_options = Options()
    browser_options.binary_location = chrome_path
    #browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--ignore-certificate-errors')
    browser_options.add_argument('--ignore-ssl-errors')
    s = Service(webdriver_path)
    browser = webdriver.Chrome(service= s, options=browser_options)
    wait = WebDriverWait(browser,20)
    return browser

#TODO
#Analyzie keywords frecuency
#save plots of work
data = None


with open('out/raw_data.json') as f:
    data = json.load(f)

browser = create_browser(chromedriver_path)
sleep(3)
def get_page(url):
    browser.get(url)
    sleep(2)
    page = browser.page_source
    with open('pog.html', 'w', encoding="utf-8") as f:
        f.write(page)
    return page

keywords_stat = {}

references_all = {}

for article in data:
    doi = article['dc:identifier']
    references_all[doi] = []
    for link in article['link']:
        if link['@ref'] == 'scidir':
            url = link['@href']
            page = get_page(url)
            #print(page)
            bs = BeautifulSoup(page, "lxml")
            
            root = bs.find("div", {"id" : "root"})
            keywords = root.find_all("div", {"class" : "keyword"})
            references = root.find_all("div", {"class" : "title text-m"})
            for k in keywords:
                keyword = k.text
                if keyword not in keywords_stat:
                    keywords_stat[keyword.lower()] = 1
                else:
                    keywords_stat[keyword.lower()] += 1
            for ref in references:
                references_all[doi].append(ref.text)

with open('out/references.json', 'w') as f:
    json.dump(references_all, f)

with open('out/keywords_stat.json', 'w') as f:
    json.dump(keywords_stat, f )
    
browser.close()       
