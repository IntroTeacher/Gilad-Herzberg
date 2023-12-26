import copy


class WordPool:
    """
    A class that acts as a pool of words. All the words in the pool are of the same length.
    """
    def __init__(self, words, word_size=None):
        """
        Constructs a WordPool.
        :param words: a list of the words to be put in the pool.
        :param word_size: optional input of the word_size
        The words will be put into the pool by the function WordPool.create_pool()
        """
        self.pool = WordPool.create_pool(words, word_size)
        self.word_size = None
        if len(self.get_words()) > 0:
            self.word_size = len(self.get_words()[0])

    def __len__(self):
        """
        Return the length of the pool.
        :return: The length of the pool.
        """
        return len(self.pool)

    def __iter__(self):
        """
        Returns an iterator to the pool
        :return: An iterator to the pool
        """
        return iter(self.pool)

    def get_words(self):
        """
        Returns a copy of the pool
        :return: A copy of the pool
        """
        return copy.deepcopy(list(self.pool))

    @staticmethod
    def is_iter(var):
        """
        Checks whether a variable is iterable
        :param var: the variable to be checked
        :return: True if var is iterable, False otherwise
        """
        try:
            _ = (i for i in var)
        except TypeError:
            return False
        return True

    @staticmethod
    def is_word(s):
        """
        Checks whether an object is a word
        :param s: the string to be checked
        :return: True if s is a word, False otherwise
        """
        if not isinstance(s, str):
            return False
        letters = [chr(i) for i in range(ord('a'), ord('z')+1)]  # get all lowercase a-z letters
        for letter in s:
            if letter.lower() not in letters:
                return False
        return True

    @staticmethod
    def create_pool(words, word_size):
        """
        Creates the word pool. The word length will be determined according to the first word in words
        :param words: List of words to be put in the pool
        :param word_size: The length of the words in the pool
        :return: The list of words in the pool
        """
        WordPool.is_iter(words)  # check if words is iterable

        pool = set()
        for word in words:  # get word length and all words afterwords
            if not WordPool.is_word(word):  # check for word containing only letters
                continue

            if word_size is None:  # assign word_size to the length of the first word
                word_size = len(word)

            if word_size != len(word):  # check for correct length
                continue

            pool.add(word.lower())

        return pool
