# Understanding depiction of Gender-based violence in newspaper articles

##  Trigger Warning:

## Abstract:

## Authors:

## Folder Structure:

The folder structure is as follows:

1. [paper_folder](paper_folder):
    - [Final Report](paper_folder/Final_paper.pdf)
2. [data](data): Contains sub-folders on all the information that was collected or results that were analyzed. Sub-folders are divided up by country and contain csvs/excel sheets for newspaper articles, results from passive voice analysis and word embedding models. Lastly, we have subfolders for analysis and manually labelled datasets as well.
    - [Mexico](data/Mexico): Data for Mexico (in Spanish)
    - [UK](data/UK): Data for the UK (in English)
    - [Pakistan](data/Pakistan): Data for Pakistan (in English)
    - [Analysis](data/analysis_results): Analysis
    - [Data Labelling](data/data_labelling): Manually Labelled GBV articles (for binary classification)
3. [notebook_experiments](notebook_experiments): Contains sub-folders with Jupyter notebooks for each aspect of the project 
    - [Binary Labelling](notebook_experiments/binary_labelling): Jupyter notebook(s) used for the purpose of binary labelling – used Pytorch and LSTM 
    - [Passive Voice](notebook_experiments/passive_voice): Jupyter notebooks used for the purpose of testing, implementing analyzing passive voice instances in GBV-related newspaper articles
    - [Word Embeddings](notebook_experiments/word_embeddings): Jupyter notebooks used for creating and analyzing word embeddings and word2vec models
4. [web_sraping](web_scraping): This folder contains all helper functions used for web-scraping newsppaer articles from top 3 newspapers in each of the following countries: Mexico, UK, Pakistan
5. [word_embedding](word_embedding):
6. [requirements.txt](requirements.text): Requirements file for this project


## Collaborators:
