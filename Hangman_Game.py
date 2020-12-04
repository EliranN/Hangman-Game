import os

SPACE = " "
ROW_SPACE = "\n"
MAX_TRIES = 6
HANGMAN_PHOTOS = {0: """x-------x""",
                  1: """x-------x\n|\n|\n|\n|\n|""",
                  2: """x--------x\n|\t\t |\n|\t\t 0\n|\n|\n|""",
                  3: """x--------x\n|\t\t |\n|\t\t 0\n|\t\t |\n|\n|""",
                  4: """x--------x\n|\t\t |\n|\t\t 0\n|\t\t/|\\\n|\n|""",
                  5: """x--------x\n|\t\t |\n|\t\t 0\n|\t\t/|\\\n|\t\t/\n|""",
                  6: """x--------x\n|\t\t |\n|\t\t 0\n|\t\t/|\\\n|\t\t/ \\\n|""",
                  }
FILE_PATH = input("Enter file path: ")
INDEX_INPUT = int(input("Enter index: "))
letter_guessed = ""
old_letters_guessed = []


def hangman_start_screen():
    """
    Print 'Hangman' start screen and user's max tries number.
    :return: None
    :rtype: None
    """
    print("""  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/
""",
          MAX_TRIES, ROW_SPACE)


def choose_word(file_path, index):
    """
    Choosing one word as secret word from file, which including words list, and return it.
    :param FILE_PATH: File path
    :param INDEX_INPUT: Index number in the words list
    :type FILE_PATH: str
    :type INDEX_INPUT: int
    :return: The selected word from relevant file, and according to index input
    :rtype: str
    """
    words_list = ""
    while not os.path.exists(file_path):
        print("Invalid path file!")
        file_path = input("Enter file path: ")
        index = int(input("Enter index: "))
    words_list_input_file = open(file_path, "r")
    for row in words_list_input_file:
        words_list = row.split(SPACE)
    words_list_input_file.close()
    while index >= len(words_list) or index < 0:
        print("Invalid index!")
        index = int(input("Enter index: "))
    selected_word = words_list[index]
    print("Let’s start!" + ROW_SPACE)
    print(HANGMAN_PHOTOS[0])
    print('_ ' * len(selected_word) + ROW_SPACE)
    return selected_word


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Trying to update the input guessed letter.
    :param letter_guessed: Input guessed letter value
    :param old_letters_guessed: Old guessed letters values
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: Returns bool value for can/can't update this letter input
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    elif not is_english_char(letter_guessed) or letter_guessed in old_letters_guessed:
        print("X")
        print(' -> '.join(sorted(old_letters_guessed)))
    else:
        print("X")
        return False


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checking if the guessed letter is valid or not.
    :param letter_guessed: Input guessed letter value
    :param old_letters_guessed: Old guessed letters values
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: Returns bool value for valid/invalid guesses
    :rtype: bool
    """
    if len(letter_guessed) == 1 and is_english_char(letter_guessed) and letter_guessed not in old_letters_guessed:
        return True
    else:
        return False


def is_english_char(letter_guessed):
    """
    Checking if the guessed letter is in English language.
    :param letter_guessed: Input guessed letter value
    :type letter_guessed: str
    :return: Returns bool value for English/Non-English language
    :rtype: bool
    """
    english_chars = "abcdefghijklmnopqrstuvwxyz"  # I tried to use isalpha() and saw this is better. We want use only English letters and not else (e.g. Hebrew letters)
    if letter_guessed in english_chars:
        return True


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Show formatted hidden word.
    :param secret_word: The secret word (which returned from 'choose_word')
    :param old_letters_guessed: Old guessed letters values
    :type secret_word: str
    :type old_letters_guessed: list
    :return: Returns guesses in the secret word, as string
    :rtype: str
    """
    current_guess = []
    for char in secret_word:
        current_guess.append("_")
    for guess_char in old_letters_guessed:
        if guess_char in secret_word:
            for i in range(0, len(secret_word)):
                if (secret_word[i] == guess_char):
                    current_guess[i] = guess_char
    current_guess = ' '.join(current_guess)
    print(current_guess)
    return current_guess


def check_win(secret_word, old_letters_guessed):
    """
    Checking if gamer winner.
    :param secret_word: The secret word
    :param old_letters_guessed: Old guessed letters values
    :type secret_word: str
    :type old_letters_guessed: list
    :return: Returns boolean if guess letter appear in secret work or not
    :rtype: bool
    """
    for char in secret_word:
        if (char not in old_letters_guessed):
            return False
    return True


def guessing():
    """
    This function for all guessing actions flow
    :return: None
    :rtype: None
    """
    num_of_tries = 0
    secret_word = choose_word(FILE_PATH, INDEX_INPUT).lower()
    while num_of_tries < MAX_TRIES:
        letter_guessed = input("Guess a letter: ").lower()
        is_valid_char = try_update_letter_guessed(letter_guessed, old_letters_guessed)
        if (is_valid_char):
            if letter_guessed not in secret_word:
                num_of_tries += 1
                print(":(")
                print(HANGMAN_PHOTOS[num_of_tries] + ROW_SPACE)
            show_hidden_word(secret_word, old_letters_guessed)
            if check_win(secret_word, old_letters_guessed):
                print("WIN")
                return
    else:
        print("LOSE")


def main():
    hangman_start_screen()
    guessing()


if __name__ == "__main__":
    main()
