""" 
NLP

Module created to describes all the functions with Natural Language Processing.
We call methods from NLTK package.
"""

import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class NLP:

    """
    A class that contais all related to Natural Language Processing.
    All the methods in this class are static.

    Attributes
    ----------

    Methods
    -------
        tokenizer(lstString : list)
            Returns the tokens of the string passed.

        filter_tokens(tokens, words_without_semantic)
            Returns the tokens without stop words, punctuation, and words without semantic meaning.
    """

    @staticmethod
    def tokenizer(lst_string):

        """
        Returns the tokens of the string passed.

        Parameters
        ----------
        lst_string : list
            String to create tokens.
        """
        
        tokens = []
        for string in lst_string:
            
            tokenize = word_tokenize(string)
            for token in tokenize:
                tokens.append(token)
        
        return tokens
    
    @staticmethod
    def filter_tokens(tokens, words_without_semantic):

        """
        Returns the tokens without stop words, punctuation, and words without semantic meaning.

        Parameters
        ----------
        tokens : list
            list of tokens to filter.  
        """
        
        filtered_tokens = list()

        for token in tokens:

            token = token.lower()

            if token not in stopwords.words("english"):
                if token not in string.punctuation:
                    if token not in words_without_semantic:
                        filtered_tokens.append(token)
                
        return filtered_tokens