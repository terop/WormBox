# WormBox

An implementation of Finnish WW2 era Vigenère cipher "Salakirjoitusviivain",
colloquially also known as "matolaatikko."

## Known limitations
 o Uses a hardcoded letter sheet. Support for reading the key from a file exists.
 o Uses hardcoded 4th group PIAEL -3+1-3-4-2 scrambling when encrypting.
 o Uses hardcoded 4th group -3+1-3-4-2 when decrypting. The key order is brute-forced.
 o Does not support the "second row". Supported replacements:
   o Swedish numerals (1->ett, 2->tva, etc.)
   o Space encoded as X
   o Period encoded as W
   o Repeating character encoded as C.

## Todo:
 o Key generation
