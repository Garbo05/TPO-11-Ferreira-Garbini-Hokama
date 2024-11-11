def load_words(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f.readlines()]
    return words


def remove_accents(word):
    accents_dictionary = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    return ''.join(accents_dictionary.get(letter, letter) for letter in word)


def validate_guess(word):
    return len(word) == 5 and word.isalpha()


def validate_word(words, word):
    word = remove_accents(word)
    return word in words
