from word_pool import WordPool
from mask import Mask


class Stack(WordPool):
    """
    A class of a stack of words. A stack is a word pool that can be filtered with masks.
    Stack includes a filter() function that can remove all elements that do not fit the mask of a specific word.
    """

    def filter(self, word, mask):
        """
        Filters the word pool according to a word and its mask relating the answer.
        :param word: The player's guess
        :param mask: The mask received
        """
        if not isinstance(mask, Mask):  # cannot filter without a mask
            return

        if len(mask.mask) != len(word):  # cannot filter with a mask with the wrong length
            return

        filtered_pool = self.pool.copy()
        for pooled_word in self.pool:
            if not mask == Mask.compute_from(pooled_word, word):
                filtered_pool.remove(pooled_word)
        self.pool = filtered_pool
        return self
