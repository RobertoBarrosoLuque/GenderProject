import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

def drop_duplicates(df: pd.DataFrame, id_col: str):
    '''
    Drops duplicated in news article df and concatenates search terms into a list
    inputs:
        df: pandas DataFrame, scraped news data
        id_col: string, col with unique identifier for article
    returns: df with no duplicates
    '''
    search_term_grouped = df.groupby(id_col)['search_term'].apply(list)
    return (df.iloc[:,:-1].drop_duplicates()).merge(search_term_grouped.reset_index(), on=id_col)

def clean_body_field(df: pd.DataFrame):
    '''
    Cleans the 'fields' column in the guardian dataframe - strips out html tags etc, and renames column
    inputs:
        df: pandas DataFrame, the guardian scraped data
    returns: df with cleaned fields column (changes column name to "body")
    '''
    df['fields'] = df.fields.str.strip("{'body': '<p>").str.strip("</p>'}")
    return df.rename(columns={'fields':'body'})

def remove_old_articles(df: pd.DataFrame):
    '''
    Removes any articles older than 2020-01-01 from articles dataframe 
    inputs:
        df: pandas DataFrame, scraped news data
    returns: df with data only from 2020-01-01 until now
    '''
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df[df['datetime'] >= '2020-01-01']

if __name__ == '__main__':

    root = Path.cwd()
    data_dir = root/"data"
    data_dir.mkdir(exist_ok=True)

    # clean guardian data
    guardian_df = pd.read_csv(data_dir/"UK/guardian_scraped.csv")
    guardian_df_no_dups = drop_duplicates(guardian_df, 'id')
    df_cleaned = clean_body_field(guardian_df_no_dups)

    guardian_df_cleaned.to_csv(data_dir/"UK/guardian_scraped_cleaned.csv", index=False)

    # clean sun data
    sun_df = pd.read_csv(data_dir/"UK/sun_scraped.csv")
    sun_df_no_dups = drop_duplicates(sun_df, 'link')
    sun_df_cleaned = remove_old_articles(sun_df_no_dups)

    sun_df_cleaned.to_csv(data_dir/"UK/sun_scraped_cleaned.csv", index=False)

    # clean times data
    times_df = pd.read_csv(data_dir/"UK/times_scraped.csv")
    times_df_no_dups = drop_duplicates(times_df, "link")

    times_df_no_dups.to_csv(data_dir/"UK/times_scraped_cleaned.csv", index=False)
