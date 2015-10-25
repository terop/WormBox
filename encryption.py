# i!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Encryption and decryption

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


class InvalidCiphertext(Exception):
    pass


# FIXME: Horizontal shift table is hardcoded until
# someone gets me a proper example table.
COL_SHIFTS = [-3, 1, -3, -4, -2]
# FIXME: Reference group number is hardcoded until
# someone gets me a proper example table.
REF_GROUP = 4  # Hardcoded for now


def find_start_pos(reference, key):
    candidates = []
    reference_set = set(reference)
    for row in range(26):
        for col in range(26):
            test_set = set([
                key[row][col],  # A
                key[0][col],    # P
                key[25][col],   # E
                key[row][0],    # L
                key[row][25],   # I
            ])
            if test_set == reference_set:
                candidates.append((row, col))

    if len(candidates) == 0:
        raise InvalidCiphertext(
            "Key reference {} not found!".format(reference))
    if len(candidates) > 1:
        raise InvalidCiphertext(
            "Key reference {} is ambiguous!".format(reference))
    return candidates[0]


def random_start_pos(key):
    import random

    good_key = False
    while not good_key:
        row = random.randrange(26)
        col = random.randrange(26)
        refgroup = "".join([
            # FIXME: hardcoded PIAEL order until someone gets me a real table
            key[0][col],
            key[row][25],
            key[row][col],
            key[25][col],
            key[row][0],
        ])
        # Make sure they key is unambiguous
        try:
            find_start_pos(refgroup, key)
            good_key = True
        except InvalidCiphertext:
            pass

    return row, col, refgroup

def is_group_ref_group(group, key):
    """Determines whether the provided group is a reference group. Returns
    True if it is and False otherwise."""
    # FIXME this is hardcoded for PIAEL order
    top_index = key[0].find(group[0])
    east_column = ''.join([key[i][25] for i in range(26)])
    east_index = east_column.find(group[1])

    if key[east_index][top_index] != group[2] or key[25][top_index] != group[3] \
    or key[east_index][0] != group[4]:
        return False

    return True

def find_ref_group(groups, key):
    """Finds the reference group from the provided group. Returns the
    group index or -1 if the group cannot be found."""
    for index, group in enumerate(groups):
        if len(group) != 5:
            return -1
        if is_group_ref_group(group, key):
            return index

    return -1

def decrypt_group(group, key, row, col):
    import string

    out = ""
    for letter in group:
        # Decryption goes from shuffled key -> permanent ruler
        ciphertext_index = str(key[row]).find(letter)
        decrypted_letter = string.ascii_uppercase[
            (ciphertext_index - col) % 26]
        out += decrypted_letter
    return out


def decrypt(ciphertext, key):
    import re

    # Only A-Z are valid. strip the rest. raise if they don't match
    packed = "".join(ciphertext.upper().split())
    filtered = "".join(re.findall(r'[A-Z]+', packed))
    if packed != filtered:
        raise InvalidCiphertext(
            "Given ciphertext contains invalid characters. "
            "Only A-Z in any case are allowed")

    groups = [packed[i:i + 5] for i in range(0, len(packed), 5)]

    ref_group_index = find_ref_group(groups, key)
    if ref_group_index == -1:
        raise InvalidCiphertext(
            "Could not find the reference group from the ciphertext")

    reference_group = groups[ref_group_index]
    del groups[ref_group_index]

    col_shift_count = 0
    row, col = find_start_pos(reference_group, key)

    decrypted_groups = []
    for group in groups:
        decrypted_group = decrypt_group(group, key, row, col)
        decrypted_groups.append(decrypted_group)
        row = (row + 1) % len(key)
        if row == 0:
            col += COL_SHIFTS[col_shift_count]
            col_shift_count = (col_shift_count + 1) % len(COL_SHIFTS)

    return " ".join(decrypted_groups)


def encrypt_group(group, key, row, col):
    encrypted = ""
    for letter in group:
        offset = ord(letter) - ord('A')
        enc_letter = key[row][(col + offset) % len(key[row])]
        encrypted += enc_letter

    return encrypted


def encrypt(plaintext, key):
    # Strip spaces and pack into groups
    plaintext = "".join(plaintext.split())
    plaintext_groups = [plaintext[i:i + 5]
                        for i in range(0, len(plaintext), 5)]

    row, col, reference = random_start_pos(key)
    col_shift_count = 0
    encrypted_groups = []
    for group in plaintext_groups:
        encrypted_groups.append(encrypt_group(group, key, row, col))
        row = (row + 1) % len(key)
        if row == 0:
            col += COL_SHIFTS[col_shift_count]
            col_shift_count = (col_shift_count + 1) % len(COL_SHIFTS)

    encrypted_groups.insert(REF_GROUP - 1, reference)

    return " ".join(encrypted_groups)
