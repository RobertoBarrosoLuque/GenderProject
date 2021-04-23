import pandas as pd
from selenium import webdriver 
from bs4 import BeautifulSoup
import bs4
import requests
import urllib.request
import time
import html5lib
import urllib.parse
import os
import requests
import time
import re
import warnings
from shutil import copyfile
import glob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import dataset
import sqlite3
warnings.filterwarnings

'''
I create separate functions for Dawn and The News for reproducaiility and clarity purposes.

I went over the robots.txt files for both these organizations' websites and I was allowed to crawl and extract
the relevant information.
'''
# DAWN
def crawl_dawn(keyword):
    '''
    This function takes a keyword as an input and searches it on Dawn's website.
    It goes back 10 pages in the search results and collects all search-results.
    Error Handling: It creates a dataframe for each page. This is appended with 
    a dataframe for the next page and so on -- this is saved for every newspaper-keyword combination
    Returns a list of links

    inputs (string): keyword
    output (list): list of links; csv created on the side
    '''

    df = pd.DataFrame([{'link': '', 'keyword': '', 'newspaper': 'dawn'}])

    prefs = {
    "download.default_directory": "",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_experimental_option('prefs', prefs)


    link_list = []
    browser = webdriver.Chrome("/Users/rukhshan/Downloads/chromedriver", chrome_options=options)
    #browser = webdriver.Chrome("/Users/rukhshan/Downloads/chromedriver")
    # searching keyword
    browser.get("https://www.dawn.com/search")
    xpath = "//input[@id='q']"
    xpath = "//input[contains(@placeholder,'Search')]"

    elem = browser.find_element_by_xpath(xpath)
    elem.send_keys(keyword)
    elem.submit()

    # defining search range
    search_range = range(1, 10)
    for number in search_range:
        number += 1
        get_links = browser.find_elements_by_xpath("(//a[@class='gs-title'])")
        
        for link in get_links:
            try:
                link = link.get_attribute('href')
                if link:
                    temp_df = pd.DataFrame([{'link': link, 'keyword': keyword, 'newspaper': 'dawn'}])
                    link_list.append(link)
                    df = df.append(temp_df)
                    df.to_csv("scraped_links_dawn_" + keyword + ".csv")
            except:
                pass

        # pause -- this is to reduce the burden of website-hits    
        time.sleep(2)
        # move onto next page
        next_page_init = "//div[@class='gsc-cursor-page'][contains(.,"
        next_page_rest = "'" + str(number) + "')]"
        next_page = next_page_init + next_page_rest
        try:
            element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, next_page)))
            #browser.find_element_by_xpath(next_page).click()
            element.click()
        except:
            print("Dawn: Error in Scraping")

    # quit browser once crawled
    browser.quit()

    return link_list

# THE NEWS
def crawl_news(keyword):
    '''
    This function takes a keyword as an input and searches it on Dawn's website.
    It goes back 10 pages in the search results and collects all search-results.
    Error Handling: It creates a dataframe for each page. This is appended with 
    a dataframe for the next page and so on -- this is saved for every newspaper-keyword combination
    Returns a list of links

    inputs (string): keyword
    output (list): list of links; csv created on the side
    '''

    df = pd.DataFrame([{'link': '', 'keyword': '', 'newspaper': 'dawn'}])

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    prefs = {
    "download.default_directory": "",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
    }

    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=options)
    link_list = []
    browser.get("https://www.thenews.com.pk/")

    #Searching keyword
    xpath = "//label[@id='search-label']"
    browser.find_element_by_xpath(xpath).click()

    xpath = "(//input[contains(@type,'text')])[2]"
    elem = browser.find_element_by_xpath(xpath)
    elem.send_keys(keyword)
    elem.submit()

    #Defining search range
    search_range = range(1, 10)

    for number in search_range:
        number += 1
        get_links = browser.find_elements_by_xpath("(//a[@class='gs-title'])")

        for link in get_links:

            try:
                link = link.get_attribute('href')
                if link:
                    temp_df = pd.DataFrame([{'link': link, 'keyword': keyword, 'newspaper': 'thenews'}])
                    df = df.append(temp_df)
                    df.to_csv("scraped_links_" + keyword + ".csv")
                    link_list.append(link)
            except:
                pass

        # pause
        # move onto next page
        time.sleep(2)
        next_page_init = "//div[@class='gsc-cursor-page'][contains(.,"
        next_page_rest = "'" + str(number) + "')]"
        next_page = next_page_init + next_page_rest

        try:
            element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, next_page)))
            element.click()
        except:
            print("The News: Error in Scraping")

    # uit browser once crawled
    browser.quit()

    return link_list


def cleanhtml(description):
    '''
    helper function to clean html -- this was not used
    '''
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', description)
    return cleantext
