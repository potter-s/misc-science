#!/usr/bin/env python3

from multiplication import MultiplicationCypher

engine = MultiplicationCypher('CONSTANTINOPLE')
message = 'fffffIhave arrivedandingoodhealthxfritz '
enc_message = engine.encrypt_message(message, 8)
print(enc_message)
dec_message = engine.decrypt_message(enc_message, 8)
print(dec_message)
