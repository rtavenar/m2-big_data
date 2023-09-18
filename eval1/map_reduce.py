def partitioner(list_of_list):
    dic_partition = {}
    for l in list_of_list :
        for cle, val in l :
            dic_partition[cle] = [val] if cle not in dic_partition else dic_partition[cle]+[val]
    return list(dic_partition.items())

def map_reduce(data, mapper, reducer):

    list_of_list_inter = map(mapper, data)
    list_inter = partitioner(list_of_list_inter)
    list_red = map(reducer, list_inter)
    
    return [(cle, val) for l in list_red for (cle, val) in l]