import requests
import json
import pandas as pd

API_KEY = 'aa845987-1fe1-473c-b622-8cc2a066da6c'
URL = 'https://content.guardianapis.com/search'
PARAMS = {'api-key': api_key, 'from-date':'2020-01-01', 'show-fields': 'body', 'page-size': 199}


def get_articles_by_term(search_term, url=URL, params=PARAMS):
    articles = []
    params['q'] = search_term
    res = call_api(params)
    articles += res['response']['results']

    for page in range(2, res['response']['pages']+1):
        params['page'] = page
        results = call_api(params)['response']['results']
        articles += results

    df = to_df(articles, search_term)

def call_api(params, api_key=API_KEY, url='https://content.guardianapis.com/search'):
    '''
    '''
    r = requests.get(url, params)
    return json.loads(r.content)

def to_df(articles, search_term):

    df = pd.DataFrame(articles)
    df['search_term'] = search_term
