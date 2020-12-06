from collections import Counter 


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
