Word-Context-Distance
=====================

Returns a Python dictionary containing a word's distance from other words within sentences or phrases from given text
returned object structure: {"word":[word's sentence positions]}

get_word_distances_per_sentence(text_to_parse, target_word, sentence_or_phrase, use_stopwords=1)
- text_to_parse => string
- sentence_or_phrase => "sentence" or "phrase" # this will further parse down sentances by , : ; breaking things into phrases as the basic unit
- target_word => string
- use_stopword => bool

Example Useage:

<code>
# get example data
import urllib2
url = "http://www.gutenberg.org/files/2554/2554.txt"
response = urllib2.urlopen(url)
raw = response.read().decode('utf8')

# get the distance data
print get_word_distances_per_sentence(raw[:111175], "sorrow", "sentence")

# the result should be
'''''''''
{u'heart': [5], u'full': [2], u'trifles': [8], u'would': [18], u'perhaps': [24], u'allow': [16], u'could': [26, 2], u'dounia': [19], u'it;': [15], u'besides': [20], u'letter': [10], u'ruin': [23], u'fill': [13]}
</code>
