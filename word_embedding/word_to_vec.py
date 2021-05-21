"""
This module holds functions used to create word embeddings based
on the word2vec algorithm developed by Mikolov et al.
See: https://arxiv.org/pdf/1310.4546.pdf for more info
"""
import pandas as pd
import numpy as np
import gensim
from pre_process.text_utils import *
import spacy
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sentiment_analysis_spanish import sentiment_analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


nlp_spanish = spacy.load("es_core_news_sm")
nlp_english = spacy.load("en_core_web_sm")


class WEmbeddings:
    def __init__(self, df: pd.DataFrame, text_col_name: str, lang="en"):
        """
        :param df: pd.DataFrame with documents to create embeddings with.
        :param text_col_name: string with name of column with text documents in df
        :param nlp: spacy pretrained model
        """
        self.main_df = df
        self.docs_index = text_col_name

        self.nlp = nlp_english if lang == "en" else nlp_spanish if lang == "es" else None

    def tokenize_normalize(self):
        """
        Clean, tokenize and normalize documents column
        """
        # Clean
        self.main_df[self.docs_index] = self.main_df[self.docs_index].apply(lambda row: clean_raw_text([row])[0])
        # Tokenize
        self.main_df['tokenized_sentences'] = self.main_df[self.docs_index].apply(lambda x:
                                                                                  [word_tokenize(s, model=self.nlp)
                                                                                   for s in sent_tokenize(x)])
        # Normalize
        self.main_df['normalized_sentences'] = self.main_df['tokenized_sentences'].apply(lambda x:
                                                                                         [normalize_tokens(s,
                                                                                          model=self.nlp) for s in x])

    def create_embedding(self):
        """
        Create word2vec embeddings of normalized sentences
        :return embedding: word2vec embedding using gensim's word 2 vec implementation
        """
        embedding = gensim.models.word2vec.Word2Vec(self.main_df['normalized_sentences'].sum(), window=10, workers=4)

        return embedding

    def __call__(self):
        self.tokenize_normalize()
        return self.create_embedding()


def convert_to_neg_pos(score):
    """
    Apply linear conversion to change into -1 to 1 range.
    :param score: float
    :return: float
    """
    new_value = ((score - 0) / (1 - 0)) * (1 + 1) + -1
    return round(new_value, 3)


SentimentScorer_span = sentiment_analysis.SentimentAnalysisSpanish()
SentimentScorer_eng = SentimentIntensityAnalyzer()


def sentiment_score(word_list, lang):
    """
    Helper function to calculate sentiment associated with word_list
    :param word_list: list of words to score
    :param lang: string with en or es
    :return sentiment: float with sentiment score for words
    """
    SentimentScorer_eng = SentimentIntensityAnalyzer()

    if lang == 'es':
        sentiment_total = [SentimentScorer_span.sentiment(word) for word in word_list]
        sentiment = convert_to_neg_pos(np.mean(sentiment_total))
    elif lang == 'en':
        sentiment = SentimentScorer_eng.polarity_scores(" ".join(word_list))
        sentiment = sentiment['compound']
    else:
        raise TypeError

    return sentiment


def extract_info_word2vec(word2vec_model, keyword, lang="en"):
    """
    Extract all relevant information for keyword in word2vec model.
    :param word2vec_model: gensim word2vec model object
    :param keyword: str with word of interest
    :return rep_words: list closest words to keyword in embedding model based on cosine dist
    :return sentiment: sentiment of closest words
    """
    try:
        words_tupple = word2vec_model.wv.most_similar(keyword)
        rep_words = [word for word, score in words_tupple]
        sentiment = sentiment_score(rep_words, lang)
    except KeyError:
        rep_words, sentiment = np.nan, np.nan

    return rep_words, sentiment


def scatter_plot_helper(fig, results, words_of_interest):
    plt.sca(fig)
    sns.scatterplot(x=results[:, 0], y=results[:, 1])
    for i, word in enumerate(words_of_interest):
        plt.scatter(results[i, 0], results[i, 1], marker='o', s=100)
        plt.annotate(word, xy=(results[i, 0], results[i, 1]))


def visualize_embeddings(embeddings_x, words_of_interest, title,  xlim=None, ylim=None):
    """
    Reduce embedding space into first and second principal components.
    Visualize words of interest using both PCA and TSNE.
    Plot scree to visualize variance explained by each PC.

    :param embeddings_x: matrix with word embeddings
    :param words_of_interest: list of words of interest to highlight
    :param title: string with title for plit
    :param xlim: list with [min, max] values for figure
    :param ylim: list with [min, max] values for figure
    :return fig: matplotlib figure object
    """
    tsne = TSNE(n_components=2, random_state=0)
    pca = PCA(n_components=10)

    result_pca = pca.fit_transform(embeddings_x)
    result_tsne = tsne.fit_transform(embeddings_x)

    sns.set_palette("Dark2")

    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(3, 2)
    pca_fig = fig.add_subplot(gs[0:2, 0])
    tsne_fig = fig.add_subplot(gs[0:2, 1])
    scree_plot = fig.add_subplot(gs[2, 0:2])

    # Plot PCA first two components
    scatter_plot_helper(pca_fig, result_pca, words_of_interest)
    plt.xlabel("PC1 scores")
    plt.ylabel("PC2 scores")
    plt.title(title + " PCA")
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)

    # Plot TSNE
    scatter_plot_helper(tsne_fig, result_tsne, words_of_interest)
    plt.xlabel("tsne_1 scores")
    plt.ylabel("tsne_2 scores")
    plt.title(title + " TSNE")

    plt.sca(scree_plot)
    sns.lineplot(x=range(1, pca.n_components+1), y=pca.explained_variance_ratio_)
    plt.xlabel("Principal component number")
    plt.ylabel("Variance explained")

    fig.tight_layout()

    return fig