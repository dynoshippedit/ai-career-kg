#!/usr/bin/env python3
print("== Frequency analysis of a Caesar cipher (shift unknown) ==")
# natural-English paragraph (letter frequencies close to real prose)
para = ("in the beginning there was only darkness and then a light appeared in the "
        "eastern sky. the people of the valley were amazed and they gathered together "
        "to see what had happened. everyone agreed that the light was a sign of better "
        "times and they celebrated for three days and three nights. even the elders, "
        "who were never easily impressed, admitted that the event was remarkable. "
        "the keeper of the records wrote the story down so that future generations "
        "would remember the night the darkness ended and the light returned to the "
        "valley forever. ")
plaintext = para * 12
SHIFT = 17
ct = "".join(chr((ord(c)-97+SHIFT) % 26 + 97) if c.isalpha() else c for c in plaintext)
from collections import Counter
freq = Counter(c for c in ct if c.isalpha())
top3 = freq.most_common(3)
print("top 3 ciphertext letters:", [(l, n) for l, n in top3])
top = top3[0][0]
guess_shift = (ord(top) - ord('e')) % 26
print(f"most common ciphertext letter: '{top}' -> guessed shift {guess_shift} (true shift {SHIFT})")
pt = "".join(chr((ord(c)-97-guess_shift) % 26 + 97) if c.isalpha() else c for c in ct)
print(f"ciphertext: {ct[:80]}...")
print(f"recovered:  {pt[:80]}...")
print("recovery successful:", pt == plaintext)
