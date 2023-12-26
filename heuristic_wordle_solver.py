import copy
from word_pool import WordPool
from stack import Stack
from mask import Mask
from wordle import Wordle
import numpy as np


class HeuristicWordleSolver:
    def __init__(self, game : Wordle):
        """
        Constructs a HeuristicWordleSolver instance.
        :param game: The game being played
        """

        self.game = game

    def choose_word(self):
        """
        Runs a computation and chooses the next word to guess
        :return: A word to be guessed
        """
        if (self.game.num_guessed == 0) and (self.game.word_size == 5):
            return 'crane'

        current_stack = Stack(self.game.get_possible_words())
        for guess in self.game.guessed:
            current_stack.filter(guess[0], guess[1])  # get the current stack

        best_guess = ('', 10**9)  # placeholder for running best guess
        for guessed_word in current_stack:  # for each word, check every target word
            sizes = []  # get stack sizes for all hypothetical target words
            # for target_word in current_stack:
            for mask in range(3**self.game.word_size):

                cloned_stack = copy.deepcopy(current_stack)
                # cloned_stack.filter(guessed_word, Mask.compute_from(guessed_word, target_word))
                cloned_stack.filter(guessed_word, Mask(*self.get_in_base_3(mask)))
                sizes.append(len(cloned_stack))
            if np.var(sizes) <= best_guess[1]:
                # print(guessed_word, np.var(sizes), sizes)
                best_guess = (guessed_word, np.var(sizes))
        return best_guess[0]

    def get_in_base_3(self, num):
        """
        Converts some number to a base 3 form in a list.
        :param num: The number to be converted
        :return: A list of digits containing num converted to base 3
        """
        result = [Mask.BLACK for i in range(self.game.word_size)]
        count = 0
        while num > 0:
            if num % 3 == 0:
                result[count] = Mask.BLACK
            if num % 3 == 1:
                result[count] = Mask.YELLOW
            if num % 3 == 2:
                result[count] = Mask.GREEN
            num //= 3
            count += 1
        return result

    def play_step(self):
        """
        Plays one step of the game
        :return: None
        """
        next_guess = self.choose_word()
        self.game.guess(next_guess)

    def won_game(self):
        """
        Checks whether the game was won.
        :return: True if the game was won, False otherwise
        """
        return self.game.won

    def lost_game(self):
        """
        Checks whether the game was lost.
        :return: True if the game was lost, False otherwise
        """
        return self.game.lost_game()
