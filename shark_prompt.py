import sys
import random
import time
import logging
from typing import List, Optional, Set


PGREEN = "\033[92m"
PRESET = "\033[0m"

logging.basicConfig(level=logging.WARN)


def load_words(word_file: Optional[str] = None) -> Set[str]:
    """Load word txt file to set

    Args:
        word_file (str): Path to text file with one word per line

    Returns:
        Set[str]: set of words loaded

    Raises:
        Exception: When file not found
    """
    if not word_file:
        logging.info("No word file")
        return set()
    with open(word_file) as f:
        return set([line.rstrip() for line in f])


class PromptPicker:
    def __init__(self, word_file, bad_word_file=None, num_words=5):
        """
        Args:
            word_file (str): Path to word file.
            bad_word_file (str, optional): Path to file containing black list. Defaults to "bad-words.txt".
            num_words (int, optional): _description_. Defaults to 5.
        """
        self.word_file = word_file
        self.num_words = num_words
        self.bad_word_list = load_words(bad_word_file)
        self.word_list = load_words(word_file)

        # check words to be filtered
        logging.debug(self.word_list.intersection(self.bad_word_list))

        # filter offensive or inappropriate words
        self.word_list = self.word_list - self.bad_word_list

    def pick_random(self) -> List[str]:
        """Pick random words from list"""
        if len(self.word_list) == 0:
            logging.warning("No words.")
        return random.sample(sorted(self.word_list), k=self.num_words)


def print_result(words):
    """Print results with formatting

    Args:
        words (list[str]): List of picked words
    """
    print(f"{PGREEN}")  # set to green
    for word in words:
        print(word, end="", flush=True)
        if word != words[-1]:
            print(", ", end="")
        time.sleep(1 / 2)
    print()
    print(f"{PRESET}")  # reset color


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        logging.warning("Word txt file not provided.")
        exit()
    picker = PromptPicker(input_file, bad_word_file="bad-words.txt")
    words = picker.pick_random()
    print_result(words)
