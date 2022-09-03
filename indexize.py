import json
from collections import defaultdict
from preprocess import preprocess


# the module that builds the inverted index
if __name__ == "__main__":

    # calls the preprocess module to get the normalized version of data
    normalized = preprocess()  # {new_id : [token_1, token_2, ..]}
    inverted_index = dict()    # {token: [new_id_1, new_id_2, ..]}
    index = defaultdict(set)
    for new_id, tokens in normalized.items():
        for token in tokens:
            index[token].add(new_id)

    inverted_index = dict()
    for new_id, tokens in index.items():
        inverted_index[new_id] = sorted(tokens)

    # dump the inverted index json into a file
    with open('index.json', 'w') as index_file:
        json.dump(inverted_index, index_file)
        index_file.close()
