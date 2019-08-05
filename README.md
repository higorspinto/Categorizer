# Categorizer

In general, Websites have their content organized into logical categories. This makes the navigation easier and findable by search engines.

This package was created to obtain the frequent categories of a set of Websites.
The module reads the categories that belong to the Websites and produces a list of common categories.
It helps when you need to produce a Website that stores categorized information from other websites.

For instance, we can create a Website that stores news from different news Websites. 
Each news has one or more categories. These different Websites categorize the news in their ways. 
Using this module we can produce just one set of categories to represent all the news from these different Websites.

## How it works

You need to create a JSON File to input the Website data into the package.

This is the format of the JSON file that you need to create:

```
[ 
	{
        "name": "NYC Open Data",
        "url": "https://opendata.cityofnewyork.us/data/",
        "categories": [
            "Business",
            "City Government",
            "Education",
            "Environment",
            "Health",
            "Housing & Development",
            "Public Safety",
            "Recreation",
            "Social Services",
            "Transportation"
        ]
	},
    {
        "name": "Chicago Open Data",
        "url": "https://data.cityofchicago.org/browse",
        "categories": [
            "Administration & Finance",
            "Buildings",
            "Community",
            "Education",
            "Environment",
            "Ethics",
            "Events",
            "FOIA",
            "Facilities & Geo. Boundaries ",
            "Health & Human Services",
            "Historic Preservation",
            "Parks & Recreation",
            "Public Safety",
            "Sanitation",
            "Service Requests",
            "Transportation"
        ]
    },
]

```

We provide a sample file to test the package. This sample file contains data from 10 American cities
Open Data Portals.

## Installing

Clone repository from git:

```
git clone https://github.com/higorspinto/Categorizer.git
```

## Using

Importing package:

```
from categorizer.categorizer import Categorizer
```

Getting a sample file from the package directory.

```
file_name = "sample_files/portals_sample.json"

```

You can pass a list of words that will not be analyzed.
These words may not have semantic content from the domains of the Websites. 
In the sample file of the package, words as "public" and "city" commonly appear on cities Open Data Portals and don't express semantic information for the categories of these Open Data Portals.

```
words_without_semantic = ["public", "city"]
```

Now we can define the number of common categories that will be returned.

```
number_of_categories = 5
```

Defining the object to call methods.

```
categorizer = Categorizer(file_name=file_name, words_without_semantic=words_without_semantic)
```

Obtaining the common words related to the Websites read from the JSON file.

```
freq_words = categorizer.common_words(number_of_categories)
print(freq_words)

```

Obtaining the common categories related to the Websites read from the JSON file.

```
common_categories = categorizer.common_categories(number_of_categories)
print(common_categories)
```

## Dependencies 

NLTK 3.4.4 (https://pypi.org/project/nltk/)

Dependencies can be installed using requirements.txt.

```
pip install -r requirements.txt
```


