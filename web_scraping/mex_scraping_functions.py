import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from htmldate import find_date
import datetime
from web_scraping.get_information import extract_article_info


def selenium_driver_helper(main_url):
    """
    Create driver object using chrome driver and selenium.
    :param main_url: string with link to main website
    :return driver: selenium driver object
    """
    # path to the chromedriver executable
    chromedriver = "C:/Users/robal/Downloads/chromedriver_win32chromedriver/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(main_url)
    return driver


def crawl_el_universal(keyword):
    """
    Crawler function to use for El Universal search website to get relevant articles about
    keyword.
    :param keyword: string
    :return all_links: list of links
    """
    main_url = "https://activo.eluniversal.com.mx/historico/search/index.php?q=" + keyword

    driver = selenium_driver_helper(main_url)

    date_now = datetime.date.today()
    date_end = datetime.date(2020, 1, 1)

    all_links = []
    while date_now > date_end:
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        rows1 = soup1.find_all("a", target="_new")
        article_links = [x.get("href") for x in rows1]
        all_links.extend(article_links)

        print(f"Working on date: {date_now}")
        print(f"Number of links processed so far: {len(all_links)}")

        date_now = pd.to_datetime(find_date(article_links[-1]))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        for button in driver.find_elements_by_xpath('.//div[@class = "Siguiente btnes"]'):
            try:
                button.click()
            except StaleElementReferenceException:
                continue

        # Check if this is the last page, if so break
        if not soup1.find_all('div', class_="Siguiente btnes"):
            break
        time.sleep(1)

    return all_links


def crawl_la_jornada(keyword):
    """
    Crawler function to use La Jornada search website to get relevant articles about
    keyword.
    :param keyword: string
    :return all_links: list of links
    """
    main_link = "https://www.jornada.com.mx/ultimas/@@search?SearchableText=" + keyword
    driver = selenium_driver_helper(main_link)

    date_now = datetime.date.today()
    date_end = datetime.date(2020, 1, 1)

    all_links = []
    while date_now > date_end:
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        rows1 = soup1.find_all('a', class_="state-published")
        article_links = [x.get("href") for x in rows1]
        all_links.extend(article_links)

        date_now = pd.to_datetime(find_date(article_links[-1]))
        print(f"Working on date: {date_now}")
        print(f"Number of links processed so far: {len(all_links)}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        for button in driver.find_elements_by_xpath('.//span[@class = "next"]'):
            button.click()

        # Check if this is the last page, if so break
        if not soup1.find_all('span', class_="next"):
            break

    # links_df = pd.DataFrame(list(zip(all_links,  ["genero" for _ in all_links], ['LaJornada' for _ in all_links])),
    #                        columns=['link', 'keyword', 'newspaper'])

    return all_links


if __name__ == '__main__':
    keyword_list = ["violación+sexual", "violencia+genero", "asesinato+mujer", "matrimonio+forzado",
                    "aborto+forzado", "agresion+sexual", "violencia+domestica", "abuso+sexual", "feminicidio"]

    # choose one from ["Universal", "LaJornada"]
    newspaper = "Universal"

    if newspaper == "Universal":
        scrape_function = crawl_el_universal
    elif newspaper == "LaJornada":
        scrape_function = crawl_la_jornada
    else:
        raise NameError(f'No webscraper function for {newspaper}')

    full_link_lst = []
    for key_word in keyword_list:
        print(f"Scraping links with keyword: {key_word}")
        links = scrape_function(key_word)
        full_link_lst.extend(links)

    print()
    print("Finished compiling all links")
    print()

    list_of_dictionaries = []
    for each_link in set(full_link_lst):
        list_of_dictionaries.append(extract_article_info(each_link))

    print()
    print("Finished extracting news information from all links")
    print()

    final_df = pd.DataFrame(list_of_dictionaries)
    final_df.to_excel('la_jornada_scraped.xlsx')
