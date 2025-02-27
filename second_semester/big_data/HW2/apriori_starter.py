from itertools import combinations
from collections import defaultdict

def read_data(file_path):
    baskets = []
    with open(file_path, 'r') as file:
        for line in file:
            baskets.append(line.strip().split())
    return baskets

def find_frequent_items(baskets, support):
    item_count = defaultdict(int)
    for basket in baskets:
        for item in basket:
            item_count[item] += 1
    return {item: count for item, count in item_count.items() if count >= support}

    
def find_frequent_pairs(baskets, frequent_items, support):
    pair_count = defaultdict(int)
    for basket in baskets:
        # TODO: Count the pairs. Check if both items are frequent before counting them.
        
        # HINT: Use frozenset() to represent pairs to ensure that the order of items does not matter, and use them as keys in a dictionary.
        filtered = [item for item in basket if item in frequent_items]
        for pair in combinations(filtered, 2):
                pair_count[frozenset(pair)] += 1
    return {pair: count for pair, count in pair_count.items() if count >= support}

def find_frequent_triples(baskets, frequent_items, frequent_pairs, support):
    triple_count = defaultdict(int)
    for basket in baskets:
        # TODO: Count the triples. Check if all items and all pairs are frequent before counting them.
        # HINT: Use frozenset() to represent pairs and triples to ensure that the order of items does not matter, and use them as keys in a dictionary.
        filtered = [item for item in basket if item in frequent_items]
        for triple in combinations(filtered, 3):
                triple_fs = frozenset(triple)
                pairs_in_triple = list(combinations(triple, 2))
                if all(frozenset(pair) in frequent_pairs for pair in pairs_in_triple):
                        triple_count[triple_fs] += 1
    return {triple: count for triple, count in triple_count.items() if count >= support}            

def apriori(baskets, support):
    frequent_items = find_frequent_items(baskets, support)
    frequent_pairs = find_frequent_pairs(baskets, frequent_items, support)    
    frequent_triples = find_frequent_triples(baskets, frequent_items, frequent_pairs, support)
    return frequent_items, frequent_pairs, frequent_triples

def compute_confidence_pairs(frequent_items, frequent_pairs):
    confidence_scores = []
    for pair, pair_support in frequent_pairs.items():
        # TODO: Generate association rules from frequent pairs and compute their confidence.
        items = list(pair)
        conf1 = pair_support / frequent_items[items[0]]
        conf2 = pair_support / frequent_items[items[1]]

        confidence_scores.append((items[0], items[1], conf1))
        confidence_scores.append((items[1], items[0], conf2))

    return sorted(confidence_scores, key=lambda x: (-x[2], x[0], x[1]))

def compute_confidence_triples(frequent_items, frequent_pairs, frequent_triples):
    confidence_scores = []
    for triple, triple_support in frequent_triples.items():
        # TODO: Generate association rules from frequent triples and compute their confidence.
        triple_list = list(triple)

        for lhs in combinations(triple_list, 2):
            lhs_fs = frozenset(lhs)
            rhs = list(triple - set(lhs))[0]
            lhs_sorted = tuple(sorted(lhs))
            conf = triple_support / frequent_pairs[lhs_fs]
            confidence_scores.append((lhs_sorted, rhs, conf))
            
    return sorted(confidence_scores, key=lambda x: (-x[2], x[0], x[1]))

def main():
    support = 100
    baskets = read_data('./browsing.txt')
    frequent_items, frequent_pairs, frequent_triples = apriori(baskets, support)
    
    # Compute and print top 5 association rules for pairs
    pair_association_rule = compute_confidence_pairs(frequent_items, frequent_pairs)
    print("Top 5 Association Rules for Pairs:")
    for lhs, rhs, confidence in pair_association_rule[:5]:
        print(f"{lhs} => {rhs}: {confidence}")

    # Compute and print top 5 association rules for triples
    triple_association_rule = compute_confidence_triples(frequent_items, frequent_pairs, frequent_triples)
    print("\nTop 5 Association Rules for Triples:")
    for lhs, rhs, confidence in triple_association_rule[:5]:
        lhs_tuple = tuple(lhs)
        print(f"{(lhs_tuple[0], lhs_tuple[1])} => {rhs}: {confidence}")

if __name__ == "__main__":
    main()