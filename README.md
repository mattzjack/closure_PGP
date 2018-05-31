# closure_PGP

- `txt2int` (and hence `int2txt`) converts ascii text to integer by concatenating 0-padded 3-digit ascii code (e.g. 'ebc' ==> 101098099), then if the integer starts with a zero, 999 is added to the front (so 'abc' ==> 999097098099). `closure_PGP` only works for text with ascii code between 0 and 998.
- Choose the modulus `N` large enough appropriately. `pub_key_encr` checks validity of the decimal number `M` encoding the message, assuming `N` is the product of 2 primes and `M` is positive.
- Exchange modulus `N` and public key `E`. Use `closure_PGP` to encode; use `closure_PGP_decode` to decode.
- Extended Euclidean algorithm, PGP protocol from Wikipedia.
