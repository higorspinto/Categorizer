# Categorizer

This package was created to obtain the frequent categories of a set of Websites.
The module reads the categories that belong to the Websites and produces a list of frequent categories.
It helps when you need to produce a Website that stores categorized information from other websites.

For instance, we can create a Website that stores news from several news websites.
Each news has one or more categories. These different websites categorized the news in their ways. 
Using this module we can produce just one set of categories to represent all the news in the several 
websites.

## Installing

'''
pip install -i https://test.pypi.org/simple/ categorizer-higorspinto==0.0.1
'''

## Using


Example:

```
from categorizer.categorizer import Categorizer

file_name = "sample_files/portals_sample.json"
words_without_semantic = ["public", "city"]
number_of_categories = 5

categorizer = Categorizer(file_name=file_name, words_without_semantic=words_without_semantic)

freq_words = categorizer.common_words(number_of_categories)
print(freq_words)

common_categories = categorizer.common_categories(number_of_categories)
print(common_categories)
```

## Dependencies 