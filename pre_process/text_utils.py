"""
Function for pre processing text. These include tokenizing words, tokenizing sentences, and normalizing.
These functions are based on those used in Computational Content Analysis lucem_illud module.
"""
import spacy
from gensim.parsing.preprocessing import STOPWORDS

try:
    nlp_english = spacy.load("en")
except OSError:
    # If you have not done so already download the pre trained models 
    # python -m spacy download en_core_news_sm
    # python -m spacy download es_core_news_sm
    nlp_english = spacy.load("en_core_web_sm")


def clean_raw_text(raw_texts):
    """
    Clean text documents during pre-processing.
    :param raw_texts: list of raw texts to pre process.
    """
    # common_stopwords = [] 
    # stopwords = [x.lower() for x in common_stopwords]
    
    clean_texts = []
    for text in raw_texts:
        try:
            clean_text = text.replace(" \'m", 
                                    "'m").replace(" \'ll", 
                                    "'ll").replace(" \'re", 
                                    "'re").replace(" \'s",
                                    "'s").replace(" \'re", 
                                    "'re").replace(" n\'t", 
                                    "n't").replace(" \'ve", 
                                    "'ve").replace(" /'d", 
                                    "'d").replace('\n','')
            
            clean_text = clean_text.rstrip(" ").rstrip(" ' ").replace("\xa0", "")
            querywords = clean_text.split()
            resultwords  = [word for word in querywords if word.lower() not in STOPWORDS]
            final_text = ' '.join(resultwords)

            clean_texts.append(final_text)
        except AttributeError:
            print("ERROR CLEANING")
            # print(text)
            continue
    return clean_texts


def word_tokenize(word_list, model=nlp_english, max_doc_sz=1500000):
    """
    Word tokenizer function, makes us of spaCy's encore_web_sm pre trained model.
    :param word_list: list of words or list with document to process.
    :param model: spacy loaded model.
    :param max_doc_sz: maximum document size that can be processed, integer for character num.
    :return tokenized: list of tokenized words in document.
    """
    tokenized = []
    if type(word_list) == list and len(word_list) == 1:
        word_list = word_list[0]

    if type(word_list) == list:
        word_list = ' '.join([str(elem) for elem in word_list]) 
    # since we're only tokenizing, I remove RAM intensive operations and increase max text size

    model.max_length = max_doc_sz
    doc = model(word_list, disable=["parser", "tagger", "ner"])
    
    for token in doc:
        if not token.is_punct and len(token.text.strip()) > 0:
            tokenized.append(token.text)
    return tokenized

def sent_tokenize(word_list, model=nlp_english):
    """
    Sentence tokenizer using spaCy models.
    :param word_list: list of words or list with document to process.
    :param model: spacy loaded model.
    """
    doc = model(word_list)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences

def normalize_tokens(word_list, extra_stop=[], model=nlp_english, lemma=True, max_doc_sz=1500000):
    """
    Normalize tokens using spacy.
    :param word_list: list of words or list with document to process.
    :param extra_stop: list of extra stop words to filter out
    :param model: spacy loaded model.
    :param lemma: boolean indicates if lemmatizing should be done
    :param max_doc_sz: maximum document size that can be processed, integer for character num.
    :return normalized: normalized list of tokens
    """
    normalized = []
    if type(word_list) == list and len(word_list) == 1:
        word_list = word_list[0]

    if type(word_list) == list:
        word_list = ' '.join([str(elem) for elem in word_list]) 

    # since we're only normalizing, I remove RAM intensive operations and increase max text size

    model.max_length = max_doc_sz
    doc = model(word_list.lower(), disable=["parser", "tagger", "ner"])

    if len(extra_stop) > 0:
        for stopword in extra_stop:
            lexeme = model.vocab[stopword]
            lexeme.is_stop = True

    # we check if we want lemmas or not earlier to avoid checking every time we loop
    if lemma:
        for w in doc:
            # if it's not a stop word or punctuation mark, add it to our article
            if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num and len(w.text.strip()) > 0:
            # we add the lematized version of the word
                normalized.append(str(w.lemma_))
    else:
        for w in doc:
            # if it's not a stop word or punctuation mark, add it to our article
            if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num and len(w.text.strip()) > 0:
            # we add the lematized version of the word
                normalized.append(str(w.text.strip()))

    return normalized