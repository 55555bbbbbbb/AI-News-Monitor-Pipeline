import json
import requests
import urllib3
from bs4 import BeautifulSoup
from pygooglenews import GoogleNews
from newspaper import Article
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_news_entries(query_base, search_days):
    start_date = (datetime.now() - timedelta(days=search_days)).strftime('%Y-%m-%d')
    gn = GoogleNews(lang='zh-TW', country='TW')
    query = f'{query_base} after:{start_date}'
    search = gn.search(query)
    return search.get('entries', [])

def get_real_url(google_rss_url):
    try:
        headers = {'user-agent': 'Mozilla/5.0'}
        resp = requests.get(google_rss_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        wiz_tag = soup.select_one('c-wiz[data-p]')
        if not wiz_tag: 
            return google_rss_url
            
        data = wiz_tag.get('data-p')
        obj = json.loads(data.replace('%.@.', '["garturlreq",'))

        payload = {'f.req': json.dumps([[['Fbv4je', json.dumps(obj[:-6] + obj[-2:]), 'null', 'generic']]])}
        post_url = "https://news.google.com/_/DotsSplashUi/data/batchexecute"
        response = requests.post(post_url, headers=headers, data=payload, timeout=10)
        
        cleaned_response = response.text.replace(")]}'", "")
        res_json = json.loads(cleaned_response)
        array_string = res_json[0][2]
        return json.loads(array_string)[1]
    except:
        return google_rss_url

def fetch_and_parse_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.encoding = response.apparent_encoding or 'utf-8'
        
        article = Article(url)
        article.set_html(response.text)
        article.parse()
        text = article.text.strip()
        
        if len(text) > 50:
            return text
    except:
        pass

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument('user-agent=Mozilla/5.0')

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)
        driver.get(url)
        text = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()
        return text
    except:
        return ""