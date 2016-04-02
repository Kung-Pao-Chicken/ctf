#Author:unamer
from pwn import *
import  gmpy2
gmpy2.get_context().precision=99999
while 1:
	err=0
	try:
		p=remote('programming.pwn2win.party','9004',ssl=1)
	except:
		err=err+1
		if err>10 : break
		continue
	s=''
	t=0
	while 1:
		s=''
		s=p.recv()
		if s.startswith('CTF-BR{') or s == 'WRONG ANSWER': break
		if 'WRONG' in s: break
		n1= gmpy2.mpz(s)
		n=gmpy2.floor((gmpy2.sqrt(n1)-1)/2)
		print 'n='+str(n)
		n2=(2*n+1)*(2*n+1)
		d=n1-n2
		print 'd='+str(d)
		v1=2*n+1
		v2=2*n+1+2*(n+1)
		v3=2*n+1+4*(n+1)
		v4=2*n+1+4*(n+1)+2*(n+1)+1
		x=0
		y=0
		if d<v1:
			x=n+1
			y=d-n
		elif d<v2:
			x=n+1-(d-v1)
			y=n+1
		elif d<v3:
			x=-n-1
			y=n+1-(d-v2)
		elif d<v4:
			x=d-v3-n
			y=-n-1
		sx=str(x)
		sy=str(y)
		if sx[-2:]=='.0': sx=sx[:-2]
		if sy[-2:]=='.0': sy=sy[:-2]
		p.sendline(sx+' '+sy)
		t=t+1
		print '==================='+str(t)+'======================='
	print s
	p.close()
	if s.startswith('CTF-BR{'): break
