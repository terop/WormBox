#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# WormBox v0.1

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

from encapsulation import marshal, unmarshal
from encryption import decrypt, encrypt, InvalidCiphertext
from key import Key

# Default key
TEST_KEY = (
    "IUFXNGLBOPTRQWMKZEYCVHJSAD\n"
    "NMIAYQPUTRVLSGZBXHDKEFWCOJ\n"
    "KDGAJIOMVHEXQNFCSYTRLBPZUW\n"
    "YVCIWRQUTXLMHOZFDGKJNSBPEA\n"
    "DFHELOPKCIQBNYMJSXGURWVATZ\n"
    "JWCGATVIXFODBKMQEYPZULRNHS\n"
    "BWFDAOSKUIEPNHVQJCGLZTXRYM\n"
    "OHELSAUYTRXDWQFPVIJMCKGNZB\n"
    "LJGUCXERWYDHPASIBVQTFOMZKN\n"
    "TOVZQSAJMDYCFHKPUIBLWNGREX\n"
    "UYDAPRKBXGMQWFLVCEZNOHSTJI\n"
    "EJSWRVAPMHNBDXCQYZUGITLKOF\n"
    "GLBYEMSDXITVHQAZWJOKUPFCNR\n"
    "ANPKLMTXVCDISWZBHGQFJYRUEO\n"
    "FCRDYELBQHXSTMOPUANZGWIKJV\n"
    "SGAIEJNQKCRDZWLOMHYBTFVXUP\n"
    "MYSBWLDXNATURJIVFGQOZPKHCE\n"
    "PTKZSYUVEONAFXCIHMDJWBQRGL\n"
    "QHTAWYDOSXGIENFJCKLZPRVMBU\n"
    "WAJMQLSFIHZPCXOYKRUEBDNVGT\n"
    "HGIASZVEPFWTQMODYKRLBNJUXC\n"
    "ZNFDPBGMUJXRQWASLHCVETOKIY\n"
    "REWGYANILMKTJBZPQCUSOVDXFH\n"
    "CBYVJUENIXTZSLWKRADFMOHQPG\n"
    "XWHNPDCJLBTIZSGEORAFMKVUYQ\n"
    "VOYWNUGIQXEZFATBDRSHLJPMCK\n"
)


def read_until_empty_line(prefix=""):
    lines = []
    while True:
        line = raw_input(prefix)
        if len(line) == 0:
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    print

    print "Loaded key:"
    key = Key(TEST_KEY)
    print key

    while True:
        print
        print "1. Encrypt"
        print "2. Decrypt"
        print "e. Exit"
        cmd = raw_input("> ")

        if cmd == "1":
            print
            print "Enter plaintext message (enter a newline to stop):"
            plaintext = read_until_empty_line("> ")

            marshaled = marshal(plaintext)
            ciphertext = encrypt(marshaled, key.key)
            print
            print "Encrypted message:"
            print ciphertext

        elif cmd == "2":
            print "Enter ciphertext message (enter a newline to stop):"
            try:
                ciphertext = read_until_empty_line("> ")
                print
                print "Decrypted message:"

                marshaled = decrypt(ciphertext, key.key)
                print "Marshaled:", marshaled

                plaintext = unmarshal(marshaled)
                print "Decrypted:", plaintext

            except InvalidCiphertext as e:
                print e

        elif cmd == "e":
            break

        else:
            print "Invalid command, try again"
