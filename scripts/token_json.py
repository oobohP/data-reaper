import urllib2
import json
import re
import argparse


class NoVariable(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def query_corpora(message_id_argument):
    """Grabs API
    with the argument being the message id of the message
    returns the contents"""

    url = EWURL
    open_url = urllib2.urlopen(url)
    result = open_url.read()
    open_url.close()
    return result


def file_open(argument_file):
    """Opens a file with the name as the argument
    defined by the user returns it"""

    try:
        with open(argument_file) as f:
            return f.read()
            f.close()
    except IOError:
        print 'the file: ', argument_file, ' was not found'


def load_json_from_api_with_key_content(api_url):
    if api_url:
        cooked_content = json.loads(api_url)
        cooked_content = cooked_content['content']
        return cooked_content
    else:
        print 'Api URL not found'


def load_json_tokens(json_argument):
    """opens the .json file for definitions then parses the data
    to a dictionary to python and returns it at the end of the func"""

    try:
        with open(json_argument) as token_file:
            tokens = json.load(token_file)
            return tokens
            token_file.close()
    except IOError:
        print 'JSON File was not found!'  # consider changing to a log


def compare_heuristic_list(cooked_list, definitions):
    """takes in a list: cooked_list and a dictionary:
    definitions. Function compares the elements in the list --
    to the keys in the dictionary. If the keys match it proceeds
    to match the items in cooked_list to the value pair of that key.
    The keys are always LIST."""

    counter = 0

    for i in set(cooked_list):
        if i in set(definitions):
            counter += 1
            print 'keys: ', i
            json_list = definitions[i]

            if json_list:
                try:
                    for i in set(cooked_list):
                        if i in set(json_list):
                            counter += 1
                            print i
                except NoVariable:
                    print 'No Variable named', NoVariable.value, 'was found.'
    # IF LOCAL VARIABLE REFERENCED BEFORE ASSSIGNMENT MEANS DOES NOT EXIST

    if counter >= 4:
        print 'Counter:', counter, ' This Message Is Probably Spam'
    else:
        print 'counter:', counter, ' Not Enough Matches || Nothing Matched'


def convert_list_string_regex(cooked_list, regex):
    """Converts a list to a string via every whitespace"""

    cooked_list = ''.join(cooked_list)
    cooked_list = re.sub(regex, '', cooked_list)
    cooked_list = cooked_list.split(' ')
    return cooked_list


def parse_cooked_content_from_corpus(message_id_argument, definitions_file):

    cooked_content = load_json_from_api_with_key_content(query_corpora(message_id_argument))
    cooked_content = cooked_content[cooked_content.find('// S'):]  # strips out urls and anything before sections
    cooked_content = cooked_content.split('\n')
    cooked_content = [i for i in cooked_content if i and not i.startswith('//')]
    cooked_content = convert_list_string_regex(cooked_content, '[a-zA-Z0-9\-!?.@#$%^&*=]{18,}')

    definitions = load_json_tokens(definitions_file)

    compare_heuristic_list(cooked_content, definitions)


if __name__ == "__main__":
    # arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument ('message_id', type = str, default = 1.0,
                        help = 'Enter Message Id From Corpus')
    parser.add_argument ('list', type = str, default = 1.0,
                        help = 'Specify token document from Current Directory')
    args = parser.parse_args()

    #
    parse_cooked_content_from_corpus(args.message_id, args.list)
