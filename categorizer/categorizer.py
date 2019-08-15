""" 
Categorizer

Module created to obtain the frequent categories of a set of Websites.
The module reads the categories from Websites and produces a list of frequent categories.
It helps when you need to produce a Website that stores categorized information from other Websites.

This module is the main module of Categorizer.
You can create this object in your code and call the methods.
"""

import json
import operator
import random 

from collections import namedtuple
from collections import Counter

from categorizer.models import Website
from categorizer.nlp import NLP

#namedtuple to store the frequency of a category - CategoryFreq(category, freq)
CategoryFreq = namedtuple('CategoryFreq', 'category freq')

class Categorizer:

    """
    A class that contains all methods and functions of the Categorizer module.

    Attributes
    ----------
    file_name : str
        the name of the file that the module will read the websites to align their categories
    
    websites: list
        list of websites that will be aligned

    words_without_semantic: list
        list of words without semantic meaning in the Websites domain.
        optional: default value is None

    _all_categories: list
        list created to store all categories from the Websites.
        store this list reduces reprocessing.
        this variable needs to treated as private.
        Call method all_categories() instead call this variable.

    Methods
    -------
    print_websites()
        Prints all websites read from file.
    
    tokenizer(string_list : list)
        Creates tokens for a list of strings.

    all_categories()
        Returns all categories of all Websites.
        Call this method instead call variable _all_categories()
    
    categories_containing_words(word : str)
        Returns the non repeated categories that contains the word.

    category_frequency(category : str)
        Returns a namedTuple - CategoryFreq(category,feq) - that represents the frequency 
        of a category in all Websites.

    max_category_frequency(lst_category_freq : list)       
        Returns a list of namedTuple - CategoryFreq(category,freq) - that have the max frequency 
        in passed list.

    common_words(num_words : int)
        Returns a list of namedTuple that represent the most frequent words in the categories 
        of all Websites.
    
    common_categories(num_categories : int)
        Returns the most frequently categories in the Websites based on the most frequent words. 
    """

    file_name : str
    websites : list
    words_without_semantic : list
    _all_categories : list #this variable needs to treated as private

    def __init__(self, file_name, words_without_semantic = None):

        self.file_name = file_name
        self.words_without_semantic = words_without_semantic

        self.websites = list()
        self._all_categories = None

        if self.words_without_semantic is None:
            self.words_without_semantic = list()

        try:

            #reads the file cointaining all Websites
            with open(file_name, 'r') as json_file: 
                data = json.load(json_file)
                for p in data:
                    #reading attributes
                    name = p['name']
                    url = p['url']
                    categories = p['categories']

                    #creating Website objects
                    website = Website(name, url, categories)
                    self.websites.append(website)

            json_file.close

        except IOError:
            print("The file cannot be opened.")

    def print_websites(self):

        """
        Prints all websites read from file.
        """

        for website in self.websites:
            print(website)

    def tokenizer(self, string_list) -> list():

        """
        Returns a list of strings tokenized and filtered.

        Parameters
        ----------
        string_list : str
            A list of strings to tokenize and filter
        """

        #Call functions from NLP module to tokenize and filter a list of strings.

        tokens = NLP.tokenizer(string_list) 
        words = NLP.filter_tokens(tokens, self.words_without_semantic)

        return words

    def all_categories(self) -> list():

        """
        Returns all the categories from all Websites.
        Call this method instead call variable _all_categories.
        
        """    

        if not self._all_categories:
            
            self._all_categories = list()

            #reads all categories from all Websites
            for website in self.websites:
                self._all_categories.extend(website.categories)

        return self._all_categories
    
    def categories_containing_word(self, word) -> list():

        """
        Returns a list of strings with non repeated categories that contains the word.

        Parameters
        ----------
        words : str
            Word to search in the categories.
        
        """
        categories = list()
        all_categories = self.all_categories()
        
        #search word in all categories
        for category in all_categories:
            
            #category needs to be tokenized as words were tokenized
            tokens = self.tokenizer([category])

            #search work in tokens of category
            if word in tokens:
                categories.append(category)

        # return non repeated categories
        return list(set(categories))
    
    def category_frequency(self, category) -> CategoryFreq:

        """
        Returns a namedTuple - CategoryFreq(category,feq) - that represents the frequency 
        of a category in all Websites.

        Parameters
        ----------
        category : str
            Category to count frequency in all categories of all Websites.
        """
        
        #counts the frequency of a category in all categories of Websites
        freq_category = self.all_categories().count(category)

        #create a namedtuple CategoryFreq to return
        categoryFreq = CategoryFreq(category = category, freq = freq_category)

        return categoryFreq

    def max_category_frequency(self, lst_category_freq) -> list() :       
        """
        Returns a list of namedTuple - CategoryFreq(category,freq) - that have the max freq 
        in passed list.

        Parameters
        ----------
        lst_category_freq : list
            List of namedTuple CategoryFreq
        """

        # obtaining the highest frequency of the categories
        # built in function max returns a namedTuple
        max_freq = max(lst_category_freq, key=lambda category_freq: category_freq.freq).freq

        highest_frequency_categories = list()
        for categoryFreq in lst_category_freq:
            # testing if the category has the same frequency of the highest frequency
            if categoryFreq.freq == max_freq:
                highest_frequency_categories.append(categoryFreq) 

        return highest_frequency_categories


    def common_words(self, num_words) -> list():

        """
        Returns a list of tuples - (word, freq) - that represent the most common words 
        in the categories of all Websites.

        Parameters
        ----------
        num_words : int
            The number of the most frequent words returned by the method.
        
        """

        #The method reads categories from all websites and creates a list of tokens
        #without stop words. Then, for each token, it counts the frequency of the token
        #in the categories of all Websites.

        #obtaining all words cointained in the categories of the websites
        all_words = self.tokenizer(self.all_categories())

        #a dict Counter to store a word as key and the frequency of the word in all categories as value
        word_freq = Counter()
        for word in all_words: 

            #if the word exists in the dict, then the frequency was already counted
            if word in word_freq: continue
                
            freq = all_words.count(word)
            word_freq.update({word : freq})

        return word_freq.most_common(num_words)

    def common_categories(self, num_categories) -> list():

        """
        Returns a list of most common categories and their frequencies in the Websites 
        based on the most frequent words. 

        Parameters
        ----------
        num_categories : int
            The number of the most frequent categories will be returned by the method.
        
        """

        #We use common words in the categories of the Websites to compose a list of common categories.
        #For each common word in the categories of all Websites, the method counts the frequency 
        #of each category that contains the common word. 
        #The most frequent category for each common word is elected as a frequent category.
        #If exists more than one frequent category, the method turns the common word a category.

        common_categories = list()

        #obtaining the common_words
        common_words = self.common_words(num_categories)

        for common_word, freq in common_words:
            
            #obtaining all categories that contain the common_word
            categories_containing_word = self.categories_containing_word(common_word)
            
            #list of namedtuples CategoryFreq
            lst_category_freq = list()

            # count the frequency of each category that contains the common_word
            for category in categories_containing_word:
                lst_category_freq.append(self.category_frequency(category))
            
            if len(lst_category_freq) == 0 : continue
            
            # a list of namedTuple with highest frequency
            highest_frequency_categories = self.max_category_frequency(lst_category_freq)

            # testing with exists only one category in highest_frequency_categories
            if len(highest_frequency_categories) == 1:
                #getting the first element
                common_categories.append(highest_frequency_categories[0])
            else:
                #turns the common word a category
                common_categories.append(CategoryFreq(category=common_word.capitalize(),freq=freq))

        #returning a list of categories instead a list of namedTuples    
        return [categoryFreq.category for categoryFreq in common_categories]


                












