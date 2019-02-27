import email
import logging
import os

seen = {}  # init once instead of clearing it every time in loop

logging.basicConfig(filename='run_time.log',
                    format='%(asctime)s:%(message)s')


def walk_email_body(file_name):
    """Takes in an .eml file, opens it and walks through
        the file in order to get the body text of the email
        the string object is converted to unicode and returned"""

    # TODO: Walk through subject as well and check for words

    body = ''  # is cleared everytime function is run

    file = open(file_name, 'r')
    email_file = email.message_from_file(file)
    file.close()

    try:
        if email_file.is_multipart():
            for part in email_file.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email_file.get_payload(decode=True)
    except IOError:
        print 'file does not exist'

    #  convert string to unicode before sending it out
    charset = email_file.get_content_charset('iso-8859-1')  # fall back
    body = body.decode(charset, 'unicode')

    return body  # unicode string


def check_if_words_are_seen(body_string):
    """Takes the unicode string and splits each word by whitespace
    appends the words to word_list. From there iterates through each word
    and adds it to a dictionary called seen. If the word does not exist
    set the value of that word to 1, otherwise add 1 to the value of that word.
    Depending on threshhold, the value of a word has to be less than a number
    but greater than another set number; This can easily be changed."""

    word_list = []  # wordlist is cleared for every eml file

    # splits the body of message per whitespace puts it in a list
    # appends it to another list called word_list to be compared later
    body_list = body_string.split()
    word_list.append(body_list)

    # in order to access the words inside of the list that's inside the list
    for words in word_list:
        for i in words:
            if i not in seen:
                seen[i] = 1
            else:
                if seen[i] >= 1:
                    seen[i] += 1
    return seen


def write_dictionary_to_list(seen_dictionary):
    """ TODO: Put the values of variable seen_dicitonary into
    a list or dictionary storage type to be returned and used"""

    for i in seen_dictionary:
        if seen_dictionary[i] < 60:  # remove too common results
            if seen_dictionary[i] >= 3:  # to be changed for user threshold
                print(i.encode('utf-8'),
                      seen_dictionary[i])  # remove ifnot windows

            """TODO: Add an else statement in case the if statement fails"""


def load_path_with_os():
    """Checks for the correct OS and changes the assets variable
    to match for the correct operating system syntax"""

    if os.name == 'mac' or 'linux':
        assets = "./assets"
    elif os.name == 'nt':
        assets = ".\\assets"

    return os.chdir(assets)


def run_database():
    """Gets all the .eml files in the current directory
    excludes a few files and runs the program to walk through
    each email. As it does this the seen dictionary is being built
    adding more keywords and adding 1 to existing keywords.
    The words are then sorted by if statements that can be changed
    in the function write_dictionary_to_list"""

    # TODO: clean this up, prob create more functions

    load_path_with_os()

    for filename in os.listdir(os.getcwd()):
        if not filename.startswith(('email_walk',
                                    'token_json',
                                    'token_definitions',
                                    'run_time.log',
                                    '._')):  # python file
            try:
                print filename
                seen_dictionary = check_if_words_are_seen(
                    walk_email_body(filename))

            except LookupError:
                print 'The Program Ran into an error on file: ', filename
                print '\n Would you like to delete this file? Y/N'
                user_input = raw_input('')

                if 'y' in user_input:
                    os.remove(filename)
                    logging.error(' Removed file:%s ', filename)

                elif 'n' in user_input:
                    continue

    # write_dictionary_to_list(seen_dictionary)


if __name__ == "__main__":
    run_database()
