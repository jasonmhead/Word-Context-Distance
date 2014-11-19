import nltk
from collections import defaultdict
from nltk.corpus import stopwords

def get_word_distances_per_sentence(text_to_parse, target_word, sentence_or_phrase, use_stopwords=1):

    if use_stopwords == 1:
        stopwords = nltk.corpus.stopwords.words('english')
    else:
        stopwords = []

    # clean up #
    target_word = target_word.lower()
    text_to_parse = clean_text(text_to_parse)

    if sentence_or_phrase == 'sentence':
        text_to_parse = text_to_parse.replace(',',' ').replace('  ',' ')
    # end cleanup #

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text_to_parse)

    if sentence_or_phrase == 'phrase':
        # split into phrases
        base_segments = []
        # split by commas
        for sentence in sentences:

            # replace other phrase punctuation with commas, and clean up
            sentence = sentence.replace(":",",").replace(";",",").replace(" ,",",").replace(", ",",")

            base_segments.append(sentence.split(','))
        sentences = flatten_list(base_segments)

    word_distance_sets = []


    # remove sentence if the taget word is not in the sentence
    valid_sentences = []
    for sentence in sentences:
        # test for a target word match # a space before or after
        target_word_pre = " "+target_word
        target_word_post = target_word+" "
        if sentence.find(target_word_pre) != -1 or sentence.find(target_word_post) != -1:
            valid_sentences.append(sentence)
    sentences = valid_sentences

    # return empty if there is no match for the target word
    if len(sentences) == 0:
        return {}

    for sent_idx, sentence in enumerate(sentences):
        word_distances = {}
        sentence = sentence.strip('.')
        words = sentence.split(' ')

        # get all word positions of the target word in sentence
        target_word_positions = [i for i, x in enumerate(words) if x == target_word]


        word_distance_sets.append({"target":[], "words":[]})

        # get the word positions of all the words
        for word in words:
            #exclude the target word and stopwords
            if word != target_word and word not in stopwords:
                word_distances[word] = [i for i, x in enumerate(words) if x == word]
        word_distance_sets[sent_idx]['target'] = target_word_positions
        word_distance_sets[sent_idx]['words']= word_distances

    # compute the distances #

    computed_distances_set = []
    # for each sentence
    for distance_set in word_distance_sets:
        computed_distances_set.append(compute_distances(distance_set["target"], distance_set["words"]))
    return merge_dicts(computed_distances_set)

def compute_distances(target_set, word_set):
    word_distances = {}
    # for each target word occurence
    for target_position in target_set:
        # for each set of word occurances
        for word,word_positions in word_set.iteritems():
            word_distances[word] = []
            # for each word position
            for word_position in word_positions:
                word_distances[word].append(abs(int(target_position)-int(word_position)))
    return word_distances

# adapted from http://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key
def merge_dicts(list_of_dicts): # where
    d = {}
    for k in list_of_dicts[0]:
        d[k] = list(d.get(k, '') for d in list_of_dicts)

    #flatten list
    for word,word_list in d.iteritems():
        d[word] = flatten_list(word_list)
    return d

def flatten_list(list_of_lists):
    flattened = [item for sublist in list_of_lists for item in sublist]

    return flattened

def clean_text(text_to_parse):
    text_to_parse = text_to_parse.replace(',',', ').replace('  ',' ').lower()
    text_to_parse = text_to_parse.replace('\r',' ').replace('\n',' ')
    text_to_parse = text_to_parse.replace('...','.').replace('..','.').replace('....','.')
    text_to_parse = text_to_parse.replace('?','.').replace('!','.')
    text_to_parse = text_to_parse.replace('---',' ').replace('--',' ').replace('_',' ')
    text_to_parse = text_to_parse.replace('*',' ')
    text_to_parse = text_to_parse.replace('(',' ').replace(')',' ')
    text_to_parse = text_to_parse.replace('[',' ').replace(']',' ')
    text_to_parse = text_to_parse.replace('{',' ').replace('}',' ')
    text_to_parse = text_to_parse.replace('"',' ')
    text_to_parse = text_to_parse.replace('   ',' ').replace('  ',' ')
    return text_to_parse

  ## the below section implements processing and application of the base word distance algorithem ##

  def remove_solo_words(distance_dict):
    no_solos = {}
    for word_idx, word_pos in distance_dict.iteritems():
        if len(word_pos) > 1:
            no_solos[word_idx] = word_pos
    return no_solos

def get_avg_distance(distance_dict, allow_solo_words = 1):
    avg_dist = {}
    if allow_solo_words != 1:
        distance_dict = remove_solo_words(distance_dict)

    for word_idx, word_pos in distance_dict.iteritems():
        avg_dist[word_idx] = sum(word_pos)/len(word_pos)
    return avg_dist;

def get_max_distance(distance_dict, allow_solo_words = 1):
    max_dist = {}
    if allow_solo_words != 1:
        distance_dict = remove_solo_words(distance_dict)

    for word_idx, word_pos in distance_dict.iteritems():
        max_dist[word_idx] = max(word_pos)
    return max_dist;

def get_min_distance(distance_dict, allow_solo_words = 1):
    min_dist = {}
    if allow_solo_words != 1:
        distance_dict = remove_solo_words(distance_dict)

    for word_idx, word_pos in distance_dict.iteritems():
        min_dist[word_idx] = min(word_pos)
    return min_dist;

def get_within_distance(distance_dict, max_distance, min_distance = 1, allow_solo_words = 1):
    within_dist = {}
    if allow_solo_words != 1:
        distance_dict = remove_solo_words(distance_dict)

    for word_idx, word_pos in distance_dict.iteritems():
        within_dist_temp = []
        for word_dist in word_pos:
            if word_dist >= min_distance and word_dist <= max_distance:
                within_dist_temp.append(word_dist) # a holder for list items that pass
        if len(within_dist_temp) > 0:
            within_dist[word_idx] = within_dist_temp
    return within_dist;

def make_distance_tree(text_to_parse, starting_target_word, max_distance = 5, tokenize_type = "sentence", min_distance = 1, max_depth = 5, allow_solo_words = 1):
    raw_initial = get_word_distances_per_sentence(text_to_parse, starting_target_word, tokenize_type) # get the starting data
    if allow_solo_words != 1:
        raw_initial = remove_solo_words(distance_dict)
    primary_dist_dict = get_within_distance(raw_initial, max_distance, min_distance, allow_solo_words)

    #start lookup recursions # this area should be eliminated and re-factored as a true recursive, tree-building function
    sent_secondaries = {}
    for dict_word, dict_counts in primary_dist_dict.iteritems():
        secondary_dist_dict = get_word_distances_per_sentence(text_to_parse, dict_word, tokenize_type)
        if len(secondary_dist_dict) > 0:
            sent_secondaries[dict_word] = secondary_dist_dict

    return sent_secondaries
