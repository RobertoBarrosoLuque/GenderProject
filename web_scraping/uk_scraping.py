import os
import time
import json
import datetime
import requests
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException        
from webdriver_manager.chrome import ChromeDriverManager
from htmldate import find_date

from web_scraping.get_information import extract_article_info

GUARDIAN_API_KEY = os.environ.get("GUARDIAN_API_KEY")

# copied here from mex_scraping_functions.py for now to add in incognito options
# move to helper misc_helper_functions.py? 
def selenium_driver_helper(main_url: str):
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
def call_api_helper(params: Dict[str, str], url: str):
    '''
    Simple requests helper functon
    input:
        params: dict with parameters for api call
        url: string of base url for requests
    returns: json requests output
    '''
    r = requests.get(url, params)
    return json.loads(r.content)

def times_scraper_helper(driver):
    '''
    BeautifulSoup helper function
    input: 
        driver: webdriver object
    returns: list of article links (or empty list if no articles are found)
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all("a", class_=None)
    if rows:
        return ['https://www.thetimes.co.uk' + x.get("href") for x in rows]
    else:
        return []

def sun_scraper_helper(driver):
    '''
    BeautifulSoup helper function
    input: 
        driver: webdriver object
    returns: list of article links (or empty list if no articles are found)
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all("a", class_="teaser-anchor teaser-anchor--search")
    if rows:
        return [x.get("href") for x in rows]
    else:
        return []


def click_selenium_helper(driver, xpath: str):
    '''
    Selenium helper function to click link
    inputs:
        driver: Selenium webdriver object
        xpath: string, the xpath of the button to click
    returns:
        True if it successfully clicks the button, False otherwise
    '''
    try:
        driver.find_elements_by_xpath(xpath)[0].click()
        return True
    except:
        return False

def get_guardian_articles_by_term(search_term: str):
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

def scrape_the_times(keyword: str):
    '''
    Scrape links of articles from The Times newspaper based on a keyword.
    input:
        keyword: string to be searched
    returns: list of strings of article links
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
    if click_selenium_helper(driver, xpath_first_page):
        all_links.extend(times_scraper_helper(driver))
        time.sleep(3)
        page = 2
        while click_selenium_helper(driver, xpath_other_pages) and page < 50:
            all_links.extend(times_scraper_helper(driver))
            page += 1
            time.sleep(3)
    return all_links


def scrape_the_sun(keyword: str):
    '''
    Scrape links of articles from The Times based on a keyword.
    input:
        keyword: string to be searched
    returns: list of strings of article links
    '''
    all_links = []
    url = 'https://www.thesun.co.uk/?s=' + keyword
    driver = selenium_driver_helper(url)
    article_links = sun_scraper_helper(driver)
    all_links.extend(article_links)
    time.sleep(2)

    for page in range(2, 51):
        url = 'https://www.thesun.co.uk/page/{}/?s='.format(page) + keyword
        if click_selenium_helper(driver, '//a[@href="'+url+'"]'):
            all_links.extend(sun_scraper_helper(driver))
            time.sleep(2)
            if page%3==0:
                time.sleep(4)
    return all_links

def get_article_info_df(links: List[str]):
    '''
    Takes a list of article urls and returns a dataframe containing article info for all links
    inputs:
        links: list of strings, the article links
    returns: pandas DataFrame containing article info for each link
    '''
    list_of_dictionaries = []
    for link in set(links):
        list_of_dictionaries.append(extract_article_info(link))
    return pd.DataFrame(list_of_dictionaries)    

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
        times_df = get_article_info_df(times_links)
        times_df['search_term'] = keyword
        times_df.to_csv(data_dir/'times_scraped.csv', mode=mode, header=header, index=False)
        mode, header = ('a', False)

    # get the sun articles
    mode, header = ('w', True)
    for keyword in keywords:
        sun_links = scrape_the_sun(keyword)
        sun_df = get_article_info_df(sun_links)
        sun_df['search_term'] = keyword
        sun_df.to_csv(data_dir/'sun_scraped.csv', mode=mode, header=header, index=False)
        mode, header = ('a', False)


