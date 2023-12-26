import copy
from word_pool import WordPool


class Mask:
    """
    A mask is the answer to a specific guess of the user. A mask is a list of numbers with the length of a word.
    Each number represents a different color, which represents the correctness of a certain letter in the guess.
    """

    BLACK = 0  # wrong letter
    YELLOW = 1  # correct letter but in a wrong spot
    GREEN = 2  # correct letter in the correct spot

    def __init__(self, *inputs, word_size=5):
        """
        Constructs a Mask instance.
        :param inputs: A tuple of the numbers inputted by the user, will be used as the mask.
        The inputs are processed by calc_input_mask
        :param word_size: The size of the mask, defaulted to be 5.
        """
        self.mask = Mask.calc_input_mask(inputs, word_size)

    def __eq__(self, other):
        """
        Checks whether two masks are the same
        :param other: The other mask
        :return: True if the two masks are equal, False otherwise.
        """
        if not isinstance(other, Mask):
            return False
        return self.mask == other.mask

    @staticmethod
    def calc_input_mask(inputs, word_size):
        """
        Processes a mask input
        :param inputs: inputs by the user.
        If the inputted mask is incomplete or too long, it will be padded with BLACKs or cropped.
        :param word_size: The length of a word.
        :return: the mask in the form of a tuple, if the word size is invalid, returns as empty tuple.
        """
        if not isinstance(word_size, int):
            return ()

        if word_size <= 0:
            return ()

        mask = []  # initialize the mask
        for inp in inputs:
            if (inp != Mask.BLACK) and (inp != Mask.YELLOW) and (inp != Mask.GREEN):  # check for input correctness
                continue

            mask.append(inp)

            if len(mask) == word_size:
                break

        while len(mask) < word_size:  # pad with BLACKs
            mask.append(Mask.BLACK)

        return tuple(mask)

    @staticmethod
    def compute_from(word, target):
        """
        Computes the mask of word in relation to target.
        :param word: The word inputted by the user
        :param target: The correct answer
        :return: A Mask, or None if the input is invalid
        """
        if (not WordPool.is_word(word)) or (not WordPool.is_word(target)):  # check for invalid inputs
            return None
        if len(word) != len(target):  # check for uneven lengths
            return None
        word_size = len(word)
        word = word.lower()
        target = target.lower()

        mask = [Mask.BLACK for _ in range(word_size)]

        used_indexes = set()  # set of indexes in the target that were used for a GREEN or a YELLOW.
        # Used to correctly manage words with the same letter twice.

        for i in range(word_size):  # check for GREENs
            if word[i] == target[i]:
                mask[i] = Mask.GREEN
                used_indexes.add(i)

        for i in range(word_size):  # check for YELLOWs
            if mask[i] == Mask.GREEN:
                continue
            for j in range(word_size):
                if (word[i] == target[j]) and (j not in used_indexes):
                    mask[i] = Mask.YELLOW
                    used_indexes.add(j)

        return Mask(*mask, word_size=word_size)
