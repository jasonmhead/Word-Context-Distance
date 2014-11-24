Word-Context-Distance
=====================

- Built by Jason Head
- jmhead@jasonhead.com
- jasonmhead.com

---------------------
This is exploratory learning code, for more complex application you might want to check out something like 
- word2vect conccept in Python: improved version with better performance than Google's word2vect: 
https://github.com/piskvorky/gensim/
- and Rosetta could be useful as well: https://github.com/columbia-applied-data-science/rosetta 
---------------------

- get_word_distances_per_sentence
- 
Returns a Python dictionary containing a word's distance from other words within sentences or phrases from given text
returned object structure: {"word":[word's positions in each sentence ]}

each target word's absoloute distance against each word in a sentence is returned

```
def get_word_distances_per_sentence(text_to_parse, target_word, sentence_or_phrase, use_stopwords=1)
```
- text_to_parse => string
- sentence_or_phrase => "sentence" or "phrase" # this will further parse down sentances by , : ; breaking things into phrases as the basic unit
- target_word => string
- use_stopword => bool

Example Useage:

```
# get example data
import urllib2, word_context_distance
url = "http://www.gutenberg.org/files/2554/2554.txt"
response = urllib2.urlopen(url)
raw = response.read().decode('utf8')

# get the distance data
print word_context_distance.get_word_distances_per_sentence(raw[:111175], "sorrow", "sentence")

# the result should be
'''''''''
{u'heart': [5], u'full': [2], u'trifles': [8], u'would': [18], u'perhaps': [24], u'allow': [16], u'could': [26, 2], u'dounia': [19], u'it;': [15], u'besides': [20], u'letter': [10], u'ruin': [23], u'fill': [13]}
```
- Utility functions for processing the result:

def get_avg_distance(distance_dict, allow_solo_words = 1)


def get_max_distance(distance_dict, allow_solo_words = 1)


def get_min_distance(distance_dict, allow_solo_words = 1)


def get_within_distance(distance_dict, max_distance, min_distance = 1, allow_solo_words = 1)

