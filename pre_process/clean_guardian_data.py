import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

def drop_duplicates(df: pd.DataFrame):
    '''
    Drops duplicated in guardian df and concatenates search terms into a list
    inputs:
        df: pandas DataFrame, guardian scraped data
    returns: df with no duplicates
    '''
    search_term_grouped = df.groupby('id')['search_term'].apply(list)
    return df = (df.iloc[:,:-1].drop_duplicates()).merge(search_term_grouped.reset_index(), on='id')

def clean_body_field(df: pd.DataFrame):
    '''
    Cleans the 'fields' column in the guardian dataframe - strips out html tags etc, and renames column
    inputs:
        df: pandas DataFrame, the guardian scraped data
    returns: df with cleaned fields column (changes column name to "body")
    '''
    df['fields'] = df.fields.str.strip("{'body': '<p>").str.strip("</p>'}")
    return df.rename(columns={'fields':'body'})

if __name__ == '__main__':

    root = Path.cwd()
    data_dir = root/"data"
    data_dir.mkdir(exist_ok=True)

    df = pd.read_csv(data_dir/"guardian_scraped.csv")

    # clean duplicates:
    df_no_duplicates = drop_duplicates(df)
    df_cleaned = clean_body_field(df_no_duplicates)

    df_cleaned.to_csv(data_dir/"guardian_scraped_cleaned.csv", index=False)
