class MultiplicationCypher():
    def __init__(self, key):
        self.set_key(key)

    # Apply a shift to a single letter
    def alph_shift(self, alph, shift):
        pos = ord(alph) - 65
        assert(pos >= 0 and pos < 26)
        pos = (pos + shift + 26) % 26 # +26 in case shift < 0
        return chr(65 + pos)

    # Apply a vector of values representing shift to the message
    # direction +1 is encrypt, -1 decrypt
    def apply_shift(self, s, v, direction):
        s2 = []
        for i in range(len(s)):
            s2.append(self.alph_shift(s[i], v[i % len(v)] * direction))
        return ''.join(s2)

    def decrypt_message(self, s, date):
        dec = []
        mk = self.mult_key(date)
        message = s.replace(' ', 'X').upper()
        dm = self.apply_shift(message, mk, -1)
        mlen = len(dm)
        while dm[mlen - 1] == 'X':
            mlen -= 1
        return dm[:mlen]

    def encrypt_message(self, s, date):
        enc = []
        mk = self.mult_key(date)
        message = self.pad_message(s.upper(), len(mk))
        return self.apply_shift(message, mk, +1)

    def set_key(self, k):
        self.key = k
        self.encode_key()

    def pad_message(self, s, kl):
        s = s.replace(' ', 'X')
        return s + 'X' * ((kl - len(s)) % kl)

    # Multiply key by constant (e.g. date) - need to include carry
    def mult_key(self, m):
        c = 0
        mk = []
        for i in range(len(self.encoded_key) - 1, -1, -1):
            r = self.encoded_key[i] * m + c
            c = r // 10
            mk.append(r % 10)
        if c:
            mk.append(c)
        return mk[::-1]

    # Encode key as a vector of 'key values' based on
    # relative position of each letter in the alphabet
    def encode_key(self):
        k = self.key
        # Add the position of each letter in the key to enable sorting
        # back to original order
        l = list(zip(k, range(len(k))))
        l = sorted(l, key = lambda x: x[0])

        # Create the key values as the third element in the list (starting with 1)
        a1, a2 = zip(*l)
        l = list(zip(a1, a2, range(1, 1 + len(k))))
        # l is now list of [letter, original position, key value]

        # Sort back to original order and extract the key value
        l = [x[2] for x in sorted(l, key = lambda x: x[1])]

        # Replace values > 9 with separate digits
        while max(l) > 9:
          m = max(l)
          i = l.index(m)
          l[i:i+1] = [m // 10, m % 10]

        self.encoded_key = l
