
""" 
Models

This module create models for the Categorizer module.
"""

class Website:

    """
    A class used to represent a Website.

    Attributes
    ----------
    name : str
        the name of the website
    url : str
        the url of the website
    categories : list
        the categories list of the website
    other_attributes : dict
        customized attributes. you can create attributes in store in a this dict.
        key is the name of the attribute and value is the value of the attribute

    Methods
    -------

    """

    name : str
    url : str
    categories : list
    other_attributes : dict

    def __init__(self, name, url, categories):

        """
        Parameters
        ----------
        name : str
            The name of the website
        url : str
            The url of the website
        categories : list
            All the categories related to the Website
        """

        self.name = name
        self.url = url
        self.categories = categories

    def __repr__(self):

        return '{self.__class__.__name__}({self.name},{self.url},{self.categories})'.format(self=self)
