import os
import time
import json
import datetime
import requests
from pathlib import Path
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException        
from webdriver_manager.chrome import ChromeDriverManager
from htmldate import find_date

from get_information import extract_article_info

GUARDIAN_API_KEY = os.environ.get("GUARDIAN_API_KEY")

# copied here from mex_scraping_functions.py for now to add in incognito options
# move to helper misc_helper_functions.py? 
def selenium_driver_helper(main_url):
    """
    Create driver object using chrome driver and selenium.
    :param main_url: string with link to main website
    :return driver: selenium driver object
    """
    # path to the chromedriver executable
    chromedriver = "C:/Users/robal/Downloads/chromedriver_win32chromedriver/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(main_url)
    return driver

# move to helper misc_helper_functions.py? 
def call_api_helper(params, url):
    '''
    Simple requests helper functon
    input:
        params: dict with parameters for api call
        url: string of base url for requests
    returns: json requests output
    '''
    r = requests.get(url, params)
    return json.loads(r.content)

def get_guardian_articles_by_term(search_term):
    '''
    Call guardian articles api for a specific search term
    input:
        search_term: string, the term to be searched in the api
    returns: DataFrame of the search results
    '''
    url='https://content.guardianapis.com/search'
    params = {'api-key': GUARDIAN_API_KEY, 'from-date':'2020-01-01',
             'show-fields': 'body', 'page-size': 199, 'q': search_term,
             'order-by': 'relevance'}
    articles = []
    res = call_api_helper(params, url)
    articles += res['response']['results']

    pages = res['response']['pages']
    stopping = min(pages, 3)

    for page in range(2, stopping+1):
        params['page'] = page
        results = call_api_helper(params, url)['response']['results']
        articles += results
    df = pd.DataFrame(articles)
    df['search_term'] = search_term
    return df

def scrape_the_times(keyword):
    '''
    '''
    all_links = []
    url = 'https://www.thetimes.co.uk/search?source=nav-desktop&filter=past_year&q=' + keyword
    driver = selenium_driver_helper(url)
    # handle cookie consent
    time.sleep(2)
    driver.switch_to_frame('sp_message_iframe_479077')
    driver.find_elements_by_xpath("/html/body/div/div[2]/div[3]/button[2]")[0].click()
    driver.switch_to.parent_frame()

    article_links = times_scraper_helper(driver)
    all_links.extend(article_links)

    time.sleep(5)

    xpath_first_page = '/html/body/section/div/div[3]/ul/li/a'
    xpath_other_pages = '/html/body/section/div/div[3]/ul/li[2]/a'

    if click_next_page(driver, xpath_first_page):
        all_links.extend(times_scraper_helper(driver))
        time.sleep(3)
        page = 2
        while click_next_page(driver, xpath_other_pages) and page < 50:
            all_links.extend(times_scraper_helper(driver))
            page += 1
            time.sleep(3)

    return all_links


def times_scraper_helper(driver):
    '''
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all("a", class_=None)
    if rows:
        return ['https://www.thetimes.co.uk' + x.get("href") for x in rows]
    else:
        return []


def click_next_page(driver, xpath):
    '''
    '''
    try:
        driver.find_elements_by_xpath(xpath)[0].click()
        return True
    except:
        return False


if __name__ == '__main__':

    root = Path.cwd()
    data_dir = root/"data"
    data_dir.mkdir(exist_ok=True)

    keywords = ["rape", "gang-rape", "gender-based violence", "honor killing", "women killed over honor", "child abuse", "forced marriage", 
                "forced abortion", "sexual assault", "domestic violence", "sexual abuse", "woman+murder"]

    # get guardian articles
    mode, header = ('w', True)
    for keyword in keywords:
        guardian_df = get_guardian_articles_by_term(keyword)
        guardian_df.to_csv(data_dir/'guardian_scraped.csv', mode=mode, header=header, index=False)
        mode, header = ('a', False)

    # get the times articles
    mode, header = ('w', True)
    for keyword in keywords:
        times_links = scrape_the_times(keyword)

        list_of_dictionaries = []
        for link in set(times_links):
            list_of_dictionaries.append(extract_article_info(link))

        times_df = pd.DataFrame(list_of_dictionaries)
        times_df['search_term'] = keyword
        times_df.to_csv(data_dir/'times_scraped.csv', mode=mode, header=header, index=False)
        mode, header = ('a', False)

