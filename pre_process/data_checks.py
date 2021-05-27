import os
import random
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List, Tuple

def get_random_subset_df(df: pd.DataFrame, n_rows: int = 100):
    '''
    Get a random subset of a df
    inputs:
        df: pandas dataframe to get a subset of
        n_rows: int, number of rows of dataframe to return (default is 100)
    returns:
        subset of n_rows of the dataframe (random rows)
    '''
    randints = random.sample(range(0, len(df)), 100)
    return df.iloc[randints, :]

def load_datasets(uk_paths, mexico_paths):
    '''
    '''
    data = {}
    for p in uk_paths:
        data[p.parents[0].name + ":" + p.stem] =  pd.read_csv(p)
    for p in mexico_paths:
        data[p.parents[0].name + ":" + p.stem] =  pd.read_excel(p)
    return data

def create_newspaper_col_pakistan(df):
    '''
    '''
    df['newspaper'] = np.where(df.link.str.contains("nation.com"), "nation", np.where(
                        df.link.str.contains("news.com"), "news", np.where(
                        df.link.str.contains("dawn.com"), "dawn", "")))
    return df

if __name__=='__main__':
    root = Path.cwd()
    data_dir = root/"data"

    # load datasets:
    uk_p = data_dir.glob('./UK/*cleaned.csv')
    uk_paths = [x for x in uk_p if x.is_file()]

    pakistan_dataset = create_newspaper_col_pakistan(pd.read_csv(data_dir/"Pakistan/pak_extracted_combined.csv"))
    pakistan_dataset_cleaned = pakistan_dataset[[x for x in pakistan_dataset.columns if not x.startswith("Unnamed")]]

    mexico_p = data_dir.glob('./Mexico/*.xlsx')
    mexico_paths = [x for x in mexico_p if x.is_file()]

    data_dict = load_datasets(uk_paths, mexico_paths)

    for news in ['dawn', 'nation', 'news']:
        data_dict["Pakistan: " + news] = pakistan_dataset_cleaned[pakistan_dataset_cleaned['newspaper'] == news]

    # create data checks (random 100 articles)
    data_check_dir = data_dir/"data_checks"
    data_check_dir.mkdir(exist_ok=True)

    for name, df in data_dict.items():
        rand_df = get_random_subset_df(df)
        filename = str(name)+"_rand100.csv"
        rand_df.to_csv(data_check_dir/filename, index=False)

    # create data labelling datasets (random 500 articles)
    data_label_dir = data_dir/"data_labelling"
    data_label_dir.mkdir(exist_ok=True)

    for name, df in data_dict.items():
        rand_df = get_random_subset_df(df)
        filename = str(name)+"_label500.csv"
        rand_df.to_csv(data_label_dir/filename, index=False)
