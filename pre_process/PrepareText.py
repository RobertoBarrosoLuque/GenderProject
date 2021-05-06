import spacy
import nltk
from nltk.stem import WordNetLemmatizer
# from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import gensim
from gensim.models import Phrases, TfidfModel
from gensim import corpora
from pre_process.text_utils import clean_raw_text

NLP = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def get_wordnet_pos(word):
    """
    Map POS tag to first character accepted by
    lemmatize method in WordNetLemmatizer class
    used to lemmatize all words in a sentence
    according to their POS tag.
    References:
    https://www.machinelearningplus.com/nlp/lemmatization-examples-python/#wordnetlemmatizerwithappropriatepostag

    :param word: text for individual word
    :type word: str
    :return: POS tag for word
    :rtype: wordnet obj
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    lemmatized_word = tag_dict.get(tag, wordnet.VERB)

    return lemmatized_word


def lemmatize_stemming(token):
    """
    Lemmatize text string.

    :param token: word in string format.
    :type token: str
    :return: lemmatized form of token
    :rtype: str
    """
    # Tokenize and lemmatize
    # stemmer = PorterStemmer()
    # for more POS tags use:
    lemmatizer = WordNetLemmatizer()
    lemmatized = lemmatizer.lemmatize(token, get_wordnet_pos(token))
    return lemmatized


def preprocess(text, min_chars=3):
    """
    Use lemmatize_stemming function and then remove all stopwords
    to return list of lematized/stemmed words in text string.

    :param text:  text for individual document
    :type text: str
    :param min_chars: minimum characters needed for a token to be included as a word
    :type min_chars: int
    :return: list of clean and lemmatized tokens
    :rtype: list
    """
    result = []
    for token in gensim.utils.simple_preprocess(text, min_len=min_chars):
        if token not in gensim.parsing.preprocessing.STOPWORDS:
            result.append(lemmatize_stemming(token))
    return result


class PrepareText:
    """
    Object implementation of pre-processing documents for Topic Modeling
    and other natural language processing methods.
    See initializer for more details.
    """

    def __init__(self, documents, bigrams=False):
        """
        Initialize PrepareText object.

        Attributes:
        - raw_text: list of string form documents
        - clean_text: preprocess and cleaned list of documents
        - dictionary: vectorized form of all documents
        - corpus: vectorized form of documents after applying bag of words
                  (t_id, t_freq)
        - corpus_tfidf: vectorized form of documents using TfIDF vectorizer
                        (t_id, t_tf_idf)

        :param documents: list of strings (each element in list is string
                          representation of a single document).
        :type documents: list
        :param bigrams: set to True to include frequent bigrams in documents.
        :type bigrams: bool
        """
        self.raw_text = documents
        self.clean_text = self.clean_all_docs(bigrams)
        self.dictionary, self.corpus, self.tfidf_corpus = self.get_corpus()

    def clean_all_docs(self, bigrams):
        """
        Clean all documents in list by tokenizing, removing short words
        removing stop words, lemmatizing and then stemming.

        :param bigrams: boolean indicating if frequent bigrams should be added.
        :type bigrams: bool
        :return: list of lists with clean/pre-processed/tokenized documents.
        :rtype: list
        """
        first_clean = clean_raw_text(self.raw_text)
        clean_docs = []
        [clean_docs.append(preprocess(text)) for text in first_clean]

        if bigrams:
            self.add_bigrams(clean_docs)
        return clean_docs

    def get_corpus(self):
        """
        Generate corpus for union of all documents.
        Where corpus is a list of list of tuples of the form:
                          [doc1 (term id, term frequency)...]

        :return dictionary: dictionary fo all documents
        :rtype dictionary: gensim corpora object
        :return corpus: vectorized form of documents (term id, frequency)
        :rtype corpus: list
        :return tfidf_corpus: vectorized form of documents (term id, tf idf score)
        :rtype tfidf_corpus: list
        """
        dictionary = corpora.Dictionary(self.clean_text)

        # vectorize into tuple (t_id, t_freq)
        corpus = [dictionary.doc2bow(text) for text in self.clean_text]

        # Convert from frequency tupple to Tf_idf
        tfidf = TfidfModel(corpus)
        tfidf_corpus = tfidf[corpus]

        return dictionary, corpus, tfidf_corpus

    def document_n(self, n):
        """
        Print out document n in original and transformed version.

        :param n: integer must be in range of len(self.raw_text)
        :type n: int
        :return: empty string
        :rtype: str
        """
        assert n in range(0, len(self.raw_text)), "Error n is out of range."

        print('Original document number:'+str(n) + '\n', self.raw_text[0]+'\n')
        print('Cleaned form of doc:\n', self.clean_text[n])
        return ''

    def add_bigrams(self, clean_text, mincount=5):
        """
        Create Bigram & Trigram Models and add them to respective documents

        :param clean_text: cleaned list of documents
        :type clean_text: list
        :param mincount: minimum count that bigram must appear to be considered.
        :type mincount: int
        """
        bigram = Phrases(clean_text, min_count=mincount)
        # trigram = Phrases(bigram[self.clean_text])

        count = 0
        for idx in range(len(clean_text)):
            for token in bigram[clean_text[idx]]:
                if '_' in token:
                    # Token is a bigram, add to document.
                    clean_text[idx].append(token)
                    count += 1
            # for token in trigram[self.clean_text[idx]]:
            #    if '_' in token:
            #        # Token is a bigram, add to document.
            #        self.raw_text[idx].append(token)
        #print('Added ', count, ' total bigrams to documents')

    def __repr__(self):
        print('First doc after cleaning:\n', self.clean_text[0])
        print('Vectorized form of first doc:\n', self.corpus[0])
        return ''
