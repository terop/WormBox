# WormBox

An implementation of Finnish WW2 era Vigenère cipher "Salakirjoitusviivain",
colloquially also known as "matolaatikko."

## Known limitations
* Uses a hardcoded letter sheet. Support for reading the key from a file exists.
* Uses hardcoded 4th group PIAEL -3+1-3-4-2 scrambling when encrypting.
* Uses hardcoded 4th group -3+1-3-4-2 when decrypting. The key order is brute-forced.
* Does not support the second row of the ruler. Supported replacements:
  * Swedish numerals (1->ett, 2->tva, etc.)
  * Space encoded as X
  * Period encoded as W
  * Repeating character encoded as C.

## Todo:
* key generation
