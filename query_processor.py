import json
from typing import List
from preprocess import normalize
import sys


# applies the postings merge algorithm, union is True for OR, False for AND
def postings_merge(list_1: List[int], list_2: List[int], union: bool) -> List[int]:
    answer = []
    l1_index, l2_index = 0, 0
    # traverse the two lists at the same time
    while l1_index < len(list_1) and l2_index < len(list_2):
        next_1 = list_1[l1_index]
        next_2 = list_2[l2_index]
        # if the elements are equal in both lists, append to answer, increment both pointers
        if next_1 == next_2:
            answer.append(next_1)
            l1_index += 1
            l2_index += 1
        # if the elements are not equal, only increment the pointer of the smaller element
        # only append to the list if union is True (OR)
        else:
            if next_1 < next_2:
                if union:
                    answer.append(next_1)
                l1_index += 1
            else:
                if union:
                    answer.append(next_2)
                l2_index += 1
    # when while is broken due to end of a list, append the remaining list if union is True (OR)
    if union:
        if l1_index <= len(list_1):
            answer.extend(list_1[l1_index:])
        if l2_index <= len(list_2):
            answer.extend(list_2[l2_index:])

    return answer


if __name__ == "__main__":

    # read the output index module has built
    with open('index.json') as index_file:
        res = json.load(index_file)
        index_file.close()

    # read the queries from the file, tokenize and normalize
    for line in sys.stdin:
        query = line.lower().replace('\n', '')
        tokenized_normalized_query = normalize(query)
        docs = res.get(tokenized_normalized_query[0])
        # keep the positive and negative query results in two different lists
        # the first word of the query is always positive
        positive_res = docs if docs is not None else []
        negative_res = []
        # depending on the logical values, add the following word's result to the correct list
        for i in range(1, len(tokenized_normalized_query) - 1):
            if i % 2 == 0:
                continue
            docs = res.get(tokenized_normalized_query[i + 1])
            docs = docs if docs is not None else []
            boolean = tokenized_normalized_query[i]
            # if it's an AND, take the conjunction of the positive list and the result new_ids for the new word
            if boolean == 'and':
                positive_res = postings_merge(positive_res, docs, False)
            # if it's an OR, take the disjunction of the positive list and the result new_ids for the new word
            elif boolean == 'or':
                positive_res = postings_merge(positive_res, docs, True)
            # if it's a NOT, take the disjunction of the negative list and the result new_ids for the new word
            elif boolean == 'not':
                negative_res = postings_merge(negative_res, docs, True)
            else:
                print('error')

        # when the query is finished, take the difference of the positive list and the negative list
        result = [word for word in positive_res if word not in negative_res]
        print(result)
