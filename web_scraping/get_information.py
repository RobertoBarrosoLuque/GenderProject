import newspaper
import time
import pandas as pd

def extract_article_info(link):
    '''
    Takes an article URL, utilizes the Python newspaper library to extract features.

    There are links that the Newspaper class is unable to identify -- for this purpose, we return a
    dictionary with None values -- we can use other text extraction methods for these as future work.

    input (string): url for article
    output (dictionary): dictionary with extracted features
    '''

    article_dict = {}
    try:
        # calling the newspaper library's Article class
        article = newspaper.Article(link) # STRING REQUIRED AS `url` ARGUMENT BUT NOT USED
        # downloading the article
        article.download()
        # parsing
        article.parse()
        # using the Article class' nlp method
        article.nlp()

        # extracting features
        article_dict['link'] = link
        article_dict['datetime'] = article.publish_date
        article_dict['title'] = article.title
        article_dict['text'] = article.text
        article_dict['authors'] = article.authors
        article_dict['summary'] = article.summary
        article_dict['keywords'] = article.keywords
        article_dict['images'] = article.fetch_images()
        article_dict['has_top_image'] = article.has_top_image()
        article_dict['top_image'] = article.top_image
        article_dict['images'] = article.images
        #article_dict['is_valid_url'] = article.is_valid_url()
        #article_dict['meta_lang'] = article.meta_lang
        #article_dict['meta_data'] = article.meta_data
        #article_dict['media_links'] = article.movies
        article_dict['successfully_scraped'] = 1

    except:
        article_dict['link'] = link
        article_dict['datetime'] = None
        article_dict['title'] = None
        article_dict['text'] = None
        article_dict['authors'] = None
        article_dict['summary'] = None
        article_dict['keywords'] = None
        article_dict['images'] = None
        article_dict['has_top_image'] = None
        article_dict['top_image'] = None
        article_dict['images'] = None
        article_dict['is_valid_url'] = None
        article_dict['meta_lang'] = None
        article_dict['meta_data'] = None
        article_dict['media_links'] = None
        article_dict['successfully_scraped'] = 0

    # pausing for 4 seconds to reduce website hits
    #time.sleep(4)

    return article_dict



def dict_to_df(dictionary):
    '''
    convert dictionary to dataframe
    input (dictionary): dictionary
    output (dataframe): dataframe
    '''

    return pd.DataFrame(dictionary)
