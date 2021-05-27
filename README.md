# Understanding depiction of Gender-based violence in newspaper articles

##  Trigger Warning:
This document and project as a whole contain references to sexual abuse, harrassment and violence.

## Abstract:
With increasing credence in the Distributional Hypothesis of language and the
development of neural network based methods to analyze textual data, there has
been a growth in the computational linguistics field to study increasingly complex
socio-cultural phenomena. Previous research has exploited the assumptions of
the distributional hypothesis to create multidimensional vector representations of
human language to investigate the presence of human bias in text. Furthermore,
word embedding (WE) models have been used to understand the semantic meaning of class and gender through time. In this work, we seek to build upon this
research by creating word embedding models of a compiled corpus, across the
political spectrum, of three newspapers in Mexico, Pakistan and the United Kingdom. We created a WE model for each of the nine newspaper corpus generated
to understand and compare how the online depiction of gender based violence
(GBV) varies across political ideology and countries. Furthermore, we developed a
methodology to identify the use of passive voice instances in text and quantified its
use across newspapers to unearth subtle linguistic indicators often used to blame
victims in sexual violence altercations. We find, by investigating the relationship between words in WE models, that there exists an increased association of
blame/responsibility dimension attributed to men in lexical space as we move from
right to left in the political spectrum. This finding is consistent in the data compiled
for both the UK and Mexico, but not for Pakistan. Moreover, we wind that, on
average, between 25% and 35% of content in online articles contain some form
of passive instances, consistent with previous research in the field. Because of
limitations in our data generating methodology, we identified non-GBV articles in
our corpus. In order to limit noise in our dataset from these non-GBV articles, we
built a recurrent neural network classifier based on the Long-Short Term Memory
(LSTM) architecture for GBV article detection. Our work identifies important
patterns in the language used in online depiction of GBV while seeking to create
an accurate Neural Network based classifier for noise reduction. In future, we hope
to use the developed classifier and the same methodologies to further understand
newspaper reporting of GBV cases.

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



