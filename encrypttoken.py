#!/usr/bin/env python
with open('token.dat', 'w') as public_file, open('token.txt') as private_file:
    for c in private_file.read().strip():
        public_file.write(hex(ord(c))[2:])
