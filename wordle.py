from word_pool import WordPool
from stack import Stack
from mask import Mask


class Wordle:
    def __init__(self, solution, allowed_guesses, num_guesses=6):
        """
        Constructs an instance of a Wordle game.
        :param solution: The target word, which the player tries to guess.
        :param allowed_guesses: The words that are allowed for guessing
        :param num_guesses: The number of guesses the player gets
        """

        if not WordPool.is_word(solution):
            return

        self.solution = solution
        self.word_size = len(self.solution)
        self.guessable_pool = WordPool(allowed_guesses, word_size=self.word_size)
        self.num_guesses = num_guesses
        self.num_guessed = None  # the number of guesses the player already used
        self.won = None  # a variable that is set to true if the player guesses correctly
        self.guessed = None  # all the guesses the player tried already
        self.restart()

    def restart(self, solution=None):
        """
        Restarts the game.
        :param solution: The solution word. If left as None the previous solution will stay.
        """
        if solution is None:
            solution = self.solution
        self.solution = solution
        self.word_size = len(self.solution)
        self.num_guessed = 0
        self.won = False
        self.guessed = []

    def get_possible_words(self):
        """
        Returns all possible guess words.
        :return: A list of possible guess words.
        """
        return self.guessable_pool.get_words()

    def lost_game(self):
        """
        Returns whether the game has been lost.
        :return: Whether the game has been lost - True or False.
        """
        return (self.num_guesses == self.num_guessed) and (not self.won)

    def guess(self, word):
        """
        Receives the player's guess, and evaluates it.
        :param word: The word the player guessed.
        :return: The mask resulted from the guess.
        """
        if self.won or self.lost_game():  # do not guess if the game is over
            return None

        if not WordPool.is_word(word):  # check for input validity
            return None
        if not len(word) == self.word_size:
            return None
        if word not in self.guessable_pool:
            return None
        self.num_guessed += 1
        mask = Mask.compute_from(word, self.solution)
        self.guessed.append((word, mask))
        self.won = sum([m == Mask.GREEN for m in mask.mask]) == self.word_size
        return mask
