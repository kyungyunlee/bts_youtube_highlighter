from collections import Counter 
import re 
import nltk


def join_timestamps(comment_dict):
    """
    Time stamps with some relaxtion of +-3 seconds 
    Returns :
        dictionary of time : [list of comments] 
    """
    all_timestamps = comment_dict.keys()
    all_timestamps_counter = dict(Counter(all_timestamps))
    all_timestamps_counter = [i[0] for i in sorted(all_timestamps_counter.items(), key=lambda k : k[1], reverse=True)]

    merged_timestamp_list = [] 
    for k in all_timestamps_counter:
        if k-3 in merged_timestamp_list or \
           k-2 in merged_timestamp_list or \
           k-1 in merged_timestamp_list or \
           k+1 in merged_timestamp_list or \
           k+2 in merged_timestamp_list or \
           k+3 in merged_timestamp_list : 
               continue 
        else : 
            merged_timestamp_list.append(k) 

    processed_timestamp_comment = {}
    for t in merged_timestamp_list : 
        processed_timestamp_comment[t] = []
        t_range = [t-3, t-2, t-1, t, t+1, t+2, t+3]
        # t_range = [t-2, t-1, t, t+1, t+2]
        for t_ in t_range : 
            try : 
                processed_timestamp_comment[t].extend(comment_dict[t_])
            except :
                continue 
    
    d = sorted(processed_timestamp_comment.items(), key=lambda x: len(x[1]), reverse=True)

    processed_timestamp_comment = {}
    for d_ in d : 
        processed_timestamp_comment[str(d_[0])] = d_[1]

    return processed_timestamp_comment



def get_timestamp_list(comment_dict):
    # list of timestamp list for distribution plot 
    timestamp_counts = [] 
    
    for k,v in comment_dict.items():
        timestamp_counts.extend([int(k)] * len(v))

    return timestamp_counts



def create_word_frequency_table(comment_list):
    stopWords_en = nltk.corpus.stopwords.words("english")
    stopWords_sp = nltk.corpus.stopwords.words("spanish")
    stopWords = set(stopWords_en + stopWords_sp)
    puncts = "'...,`;:?!''/-\\)(><][|&@#$%^*"
    timepattern = "(?:([0-5]?[0-9]):)?([0-5]?[0-9]):([0-5][0-9])"
    names = ['😂😂', '😂😂😂', '😂😂😂😂', '``', '...', '....', '.....', '--', 'rapmon','jeon', 'min', 'kim', 'park', 'yoongi', 'seokjin', 'hoseok', 'jimin', 'bts', 'jungkook', 'hobi', 'jin', 'v', 'j-hope', 'taehyung', 'kookie','jhope', 'tae', 'suga', 'rm', 'namjoon', 'jk']

    
    sentences = " ".join(comment_list)
    words = nltk.tokenize.word_tokenize(sentences)
    ps = nltk.stem.PorterStemmer()
    freqTable = {}
    for word in words :
        stem_word = word 
        stem_word = stem_word.lower()
        if stem_word in puncts : 
            continue 
        elif stem_word in stopWords : 
            continue 
        elif stem_word in names : 
            continue 
        elif re.match(timepattern, stem_word):
            continue 

        elif stem_word in freqTable.keys():
            freqTable[stem_word] +=1
        else :
            freqTable[stem_word] = 1 

    sorted_dict = {k:v for k, v in sorted(freqTable.items(), key=lambda item:item[1], reverse=True)}
    count = 0 
    keywords = []

    for k,v in sorted_dict.items():
        if "'" in k or " " in k :
            continue
        if len(k) == 1 and (k!="v" or k!="V"):
            continue
        
        if count > 2000:
            break 

        keywords.append((k,v))
        count+=1
        
    return keywords 








