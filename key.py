#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Key reader for WormBox

# The MIT License (MIT)

# Copyright (c) 2015 Antti Nilakari

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Authors
# Antti Nilakari <antti.nilakari@gmail.com>


"""
The Key class represents the 'letter matrix' part of the encryption key.

The worm box uses a sheet with 26 lines of 26 letters each.
Each line contains the full english A to Z alphabet with
individual etters shuffled. The letters may be placed in their
natural position (e.g. the line may start with an A) and the same letter
is allowed to appear multiple times in the same column.

The key reader attempts to be as permissive as possible
and only cares about the end result.
"""


class Key(object):
    import string

    # Number of valid lines in a key
    LINES_IN_KEY = 26
    # Set of valid characters
    VALID_CHARS = set(string.ascii_uppercase)

    # Raised if any part of the
    class InvalidKey(Exception):
        pass

    class InvalidLine(Exception):
        pass

    @classmethod
    def read_and_validate(cls, keystream):
        keylines = []
        keystream_lines = keystream.readlines()
        if len(keystream_lines) < 26:
            raise cls.InvalidKey("Key has less than 26 lines")

        for line in keystream_lines:
            keyline = cls.read_and_validate_line(line)
            keylines.append(keyline)

        if len(keylines) != cls.LINES_IN_KEY:
            print len(keylines)
            raise cls.InvalidKey("Key was invalid")
        return keylines

    @classmethod
    def read_and_validate_line(cls, line):
        keychars = []
        used_chars = set()

        for char in line:
            # Ignore whitespace
            if char.isspace():
                continue
            # Key is saved in uppercase format
            char_case = char.upper()
            if char_case in used_chars:
                raise cls.InvalidLine("Character {} found "
                                      "multiple times in line '{}'".format(
                                          char, line))
            used_chars.add(char_case)
            keychars.append(char_case)

        # If the key was not a perfectly shuffled
        # character range, raise
        if used_chars != cls.VALID_CHARS:
            raise cls.InvalidLine(
                "Line '{}' is not a valid keyline".format(line))
        return "".join(keychars)

    def __init__(self, keystream):
        if isinstance(keystream, str):
            import StringIO
            keystream = StringIO.StringIO(keystream)
        self.key = self.read_and_validate(keystream)

    def __str__(self):
        return "\n".join([
            " ".join(line) for line in self.key
        ])
