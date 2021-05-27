# Understanding depiction of Gender-based violence in newspaper articles

##  Trigger Warning:
This document and project as a whole contain references to sexual abuse, harrassment and violence.

## Abstract:

## Authors:
- Caitlin Loftus
- Roberto Barroso Luque
- Rukhshan Arif Mian

## Acknowledgements:
We would like to thank the following people for their support throughout this project:
1. Professor Amitabh Chaudhary (University of Chicago)
2. Jenny Long (University of Chicago)
3. Rosa Zhou (University of Chicago)

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
3. [analyses](analyses): Contains sub-folders with Jupyter notebooks for each aspect of the project 
    - [Binary Labelling](analyses/binary_labelling): Jupyter notebook(s) used for the purpose of binary labelling – used Pytorch and LSTM 
    - [Passive Voice](analyses/passive_voice): Jupyter notebooks used for the purpose of testing, implementing analyzing passive voice instances in GBV-related newspaper articles
    - [Word Embeddings](analyses/word_embeddings): Jupyter notebooks and Python script used for creating and analyzing word embeddings and word2vec models
4. [web_sraping](web_scraping): This folder contains all helper functions used for web-scraping newsppaer articles from top 3 newspapers in each of the following countries: Mexico, UK, Pakistan
5. [pre_process](pre_process): Pre-processing functions to clean and process newspaper articles.
6. [requirements.txt](requirements.text): Requirements file for this project



