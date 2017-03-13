import os, itertools
from collections import Counter

def file_to_list(file_name):
    """Read a text file and create a list containing lines from the file.
    Args:
        file_name: String of name and extension of the file.
    Returns:
        List of lines.
    """
    fr = open(file_name, encoding = 'utf-8')
    l = [line.strip() for line in fr]
    fr.close()
    return l

def list_to_set(l):
    """Create a set from a list."""    
    s = { item for item in l }
    return s
    
def get_main_words(idioms_set):
    """Get main words from a list of idioms.
    Prints an object with all main words and frequencies. Prints an object with 50 most frequent.
    Args:
        idioms_set: Set of strings of idioms.
    Returns:
        List of main words.
    """
    main_words = Counter([idiom.split()[-1] for idiom in idioms_set])
    print('main words:', '\n', main_words)
    print('top 50 main words:', '\n', main_words.most_common(50))    
    return list(main_words)
    
def get_power_expressions(idioms_set):
    """Get power expressions from a list of idioms.
    Prints an object with all power expressions and frequencies. Prints an object with 50 most frequent.
    Args:
        idioms_set: Set of strings of idioms.
    Returns:
        List of power expressions.
    """
    power_expressions = Counter([' '.join(idiom.split()[:-1]) for idiom in idioms_set])
    print('power expressions:', '\n', power_expressions)
    print('top 50 power expressions:', '\n', power_expressions.most_common(50))    
    return list(power_expressions)

def list_to_file(l, file_name):
    """Create a text file containing a list."""
    fw = open(file_name, 'w', encoding = 'utf-8')
    fw.write('\n'.join(l))
    fw.close()

def get_all_pairs(idioms_set, power_expressions, main_words):
    """Get all possible combimations of 'power expression + main word' except for those in the set of idioms.
    Create a text file with all pairs.
    Args:
        idioms_set: Set of strings of idioms.
        power_expressions: List of power expressions.
        main_words: List of main words.
    Returns:
        List of all pairs.
    """
    print('getting all pairs...')
    all_pairs = [' '.join(pair) for pair in list(itertools.product(power_expressions, main_words)) if ' '.join(pair) not in idioms_set]
    list_to_file(all_pairs, 'all_pairs.txt')
    print('file all_pairs.txt created')
    return all_pairs

def get_best_endings(idioms_set, main_words):
    """Get the best(most frequent) ending of a power expression for each main word from the set of idioms.
    Args:
        idioms_set: Set of strings of idioms.
        main_words: List of main words.
    Returns:
        Dictionary {main word: best ending}.
    """
    best_endings = {}
    for word in main_words:
        endings = Counter([' '.join(idiom.split()[:-1])[-2:] for idiom in idioms_set if idiom.split()[-1] == word])
        best_endings[word] = endings.most_common(1)[0][0]
    return best_endings

def get_good_pairs(idioms_set, power_expressions, main_words, all_pairs):
    """Get all good combimations of 'power expression + main word' except for those in the set of idioms.
    Create a text file with good pairs.
    Args:
        idioms_set: Set of strings of idioms.
        power_expressions: List of power expressions.
        main_words: List of main words.
        all_pairs: List of all pairs.
    Returns:
        List of good pairs.
    """
    print('getting good pairs...')
    best_endings = get_best_endings(idioms_set, main_words)
    good_pairs = [pair for pair in all_pairs if best_endings[pair.split()[-1]] == pair.split()[-2][-2:]]
    list_to_file(good_pairs, 'good_pairs.txt')
    print('file good_pairs.txt created')
    return good_pairs
    
idioms_list = file_to_list('idioms_high.txt')
idioms_set = list_to_set(idioms_list)
main_words = get_main_words(idioms_set)
power_expressions = get_power_expressions(idioms_set)
all_pairs = get_all_pairs(idioms_set, power_expressions, main_words)
good_pairs = get_good_pairs(idioms_set, power_expressions, main_words, all_pairs)