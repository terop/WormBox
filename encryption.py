#i!/usr/bin/env python
# -*- encoding: utf-8 -*-


# Encryption and decryption

# MIT License
# FIXME: Insert full license text here
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


def decrypt_group(group, key, row, col):
	import string

	out = ""
	for letter in group:
		# Decryption goes from shuffled key -> permanent ruler
		ciphertext_index = str(key[row]).find(letter)
		decrypted_letter = string.ascii_uppercase[(ciphertext_index - col) % 26]
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

	try:
		reference_group = groups[REF_GROUP - 1]
		del groups[REF_GROUP - 1]
	except IndexError:
		reference_group = groups[-1]
		del groups[-1]

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
	
