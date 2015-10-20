#!/usr/bin/env python
# -*- encoding: utf-8 -*-


# Encapsulation and deencapsulation of messages
# sent over WormBox

# MIT License
# FIXME: Insert full license text here
# Antti Nilakari <antti.nilakari@gmail.com>


# Number to word mapping table
NUMBER_MAPPING = [
    'NOL', 'ETT', 'TVA', 'TRE', 'FYR',
    'FEM', 'SEH', 'SJU', 'AHT', 'NIE',
]


# Maps a digit from a regex to a matching word
def re_digit_to_word(match):
    number = int(match.group(0))
    return NUMBER_MAPPING[number]


# Maps a word from a regex to a matching digit
def re_word_to_digit(match):
    word = match.group(0)
    if word in NUMBER_MAPPING:
        return str(NUMBER_MAPPING.index(word))
    else:
        return word


# Encapsulate the message
def marshal(message):
    import re

    # Uppercase first for easier processing
    message_out = message.upper()

    # Number and other special character replacement
    # FIXME: is this subject to consecutive letter
    # substitution?
    # FIXME: are spaces entered between words?
    message_out = re.sub(r'(\d)', re_digit_to_word, message_out)
    message_out = re.sub(r'\.', 'W', message_out)
    # These cannot be autoconverted back!
    message_out = re.sub('Å', 'AA', message_out)
    message_out = re.sub('Ä', 'AE', message_out)
    message_out = re.sub('Ö', 'OE', message_out)

    # Consecutive characters are escaped as C
    # FIXME: if the consecutive letters are sent in different
    # five-letter groups, should they be replaced or not?
    message_out = re.sub(r'([ABD-YZ])\1', r'\1C', message_out)

    # Heading and trailing space are done away with
    # and the remains are converted to a single X
    message_out = 'X'.join(message_out.split())

    # Pack in groups of five
    message_out = ' '.join([
        message_out[i:i + 5].ljust(5, 'X')
        for i
        in range(0, len(message_out), 5)
    ])

    return message_out


# Deencapsulate
def unmarshal(message):
    import re

    # Easier to handle in upper case
    message_in = message.upper()

    # Remove any inter-group spaces
    message_in = ''.join(message_in.split())

    # Replace C with previous letter
    message_in = re.sub(r'([ABD-YZ])C', r'\1\1', message_in)

    # Reinsert spaces
    message_in = re.sub(r'X', r' ', message_in)

    # Reinsert numbers
    message_in = re.sub(
        r'((NOL)|(ETT)|(TVA)|(TRE)|(FYR)|(FEM)|(SEH)|(SJU)|(AHT)|(NIE))+?',
        re_word_to_digit,
        message_in)
    message_in = re.sub('W', '.', message_in)

    return message_in
