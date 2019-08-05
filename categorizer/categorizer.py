""" 
Categorizer

Module created to align categories of different websites.
The module reads the categories that belong to the websites and produces a list of frequent categories
in the Websites.
It helps when you need to produce a Website that stores categorized information from other websites.

For instance, we can create a Website that stores news from several news websites.
Each news has one or more categories. These different websites categorized the news in their ways. 
Using this module we can produce just one set of categories to represent all the news in the several 
websites that we want to read and store or refer them to just one website.

This module is the main module of Categorizer.
You can create this object in your code and call the methods.
"""

import json
import operator
import random 

from collections import namedtuple
from collections import OrderedDict

from models import Website
from nlp import NLP

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
        Call method all_categories() instead call this variable

    Methods
    -------
    print_websites()
        Prints all websites read from file.
    
    tokenizer(string_list : list)
        Creates tokens for a list of strings.

    all_categories()
        Returns all categories of all Websites.
        Call this method instead call variable _all_categories()
    
    categories_containing_words()
        Returns the categories that contains the word.

    common_words(num_words : int)
        Returns the most frequent words in the categories of all Websites.
    
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
        Call functions from NLP module to tokenize and filter a list of strings.
        Returns a list of strings tokenized and filtered.

        Parameters
        ----------
        string_list : str
            A list of strings to tokenize and filter
        """

        tokens = NLP.tokenizer(string_list) 
        words = NLP.filter_tokens(tokens, self.words_without_semantic)

        return words

    def all_categories(self) -> list():

        """
        Returns all the categories from all Websites.
        Call this method instead call variable _all_categories
        
        """    

        if not self._all_categories:
            #reads all categories from all Websites
            self._all_categories = list()
            for website in self.websites:
                self._all_categories.extend(website.categories)

        return self._all_categories
    
    def categories_containing_word(self, word) -> list():

        """
        Returns the categories that contains the word.

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

        return categories
    
    def category_frequency(self, category) -> CategoryFreq:

        """
        Returns the frequency of a category in all Websites.

        Parameters
        ----------
        category : str
            Category to count frequency in all categories of all Websites.
        """
        
        all_categories = self.all_categories()
        
        #counts the frequency of a category in all categories of Websites
        freq_category = all_categories.count(category)

        #create a namedtuple CategoryFreq to return
        categoryFreq = CategoryFreq(category = category, freq = freq_category)

        return categoryFreq


    def common_words(self, num_words):

        """
        Returns the most frequent words in the categories of all Websites.

        The method reads categories from all websites and creates a list of tokens
        without stop words. Then, for each token, it counts the frequency of the token
        in the categories of all Websites.

        Parameters
        ----------
        num_words : int
            The number of the most frequent words returned by the method.
        
        """
        words = self.tokenizer(self.all_categories())

        #dict to store a word as key and the frequency of the word in all categories as value
        dict_word_freq = dict()
        for word in words: 

            #if the word exists in the dict, then the frequency was already counted
            if word in dict_word_freq: continue
                
            freq_word = words.count(word)
            dict_word_freq.update({word : freq_word})

        #create a dict ordered by frequency of word
        dict_word_freq_ord = OrderedDict(sorted(dict_word_freq.items(),
                            key = operator.itemgetter(1),
                            reverse = True))

        #returns the first (num_words) words in the list of dict keys
        return list(dict_word_freq_ord.keys())[:num_words]

    def common_categories(self, num_categories):

        """
        Returns the most frequent categories in the Websites based on the most frequent words. 
        
        We use common words in the categories of the Websites to compose a list of common
        categories.
        For each common word in the categories of all Websites, the method counts the frequency 
        of each category that contains the common word. 
        The most frequent category for each common word is elected as a frequent category.
        If exists more than one frequent category, the method randonly chooses one of the frequent
        category list.

        This method may return similar categories. Then you can choose if you want to use 
        all categories returned or some of them.

        Parameters
        ----------
        num_categories : int
            The number of the most frequent categories will be returned by the method.
        
        """

        common_categories = list()

        #obtaining the common_words
        common_words = self.common_words(num_categories)

        for common_word in common_words:
            
            #obtaining all categories that contain the common_word
            categories_containing_word = self.categories_containing_word(common_word)
            
            #list of namedtuples CategoryFreq
            lst_category_freq = list()

            # count the frequency of each category that contains the common_word
            for category in categories_containing_word:
                lst_category_freq.append(self.category_frequency(category))
            
            if len(lst_category_freq) == 0 : continue

            # sorting list of namedtuples CategoryFreq
            lst_category_freq.sort(key=lambda r: r.freq, reverse=True)

            # obtaining the highest frequency of the categories
            # the highest_frequency is in the first element of the list,
            # since the list is sorted in frequency order
            highest_frequency = lst_category_freq[0].freq

            # other categories may have the same frequency
            # so we randomly choose one category 
            highest_frequency_categories = list()
            for categoryFreq in lst_category_freq:

                # testing if the category has the same frequency of the highest frequency
                if categoryFreq.freq == highest_frequency:
                    # testing if one equal category exists in the list of common categories
                    if categoryFreq.category not in common_categories:
                        # adding all highest frequent categories in the common categories list 
                        highest_frequency_categories.append(categoryFreq.category) 
                else:
                    # if the frequency of a category is less than the highest frequent category,
                    # it doesn't need to test anymore.
                    break

            #randomly choose one category from the highest frequency list
            common_categories.append(random.choice(highest_frequency_categories))
            
        return common_categories


                












