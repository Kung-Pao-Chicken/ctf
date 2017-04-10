&nbsp;&nbsp;When connecting to the challenge server, it gives us a strange string. 

![Alt initial](./images/initial.png?raw=true)

&nbsp;&nbsp;File command says it is zlib compressed string. Well then, just use a script to decompress it everytime (what is send to the server should also be zlib compressed). 

![Alt shacolla01](./images/shacolla01.png?raw=true)

&nbsp;&nbsp;We are required to send two different strings with same sha1 value. It is easy to recall the two pdfs with same sha1 that Google release several weeks ago. First 320 byte of the two files are different. 

&nbsp;&nbsp;Experiments show that, if we use the different first 320 bytes and a same suffix to construct a string, their sha1 will also be the same. The sha1 should end with certain 5 bytes, but this is easily worked out with brute force. So again write a script (kinda ugly though)

```
import zlib
import hashlib
from pwn import *
m=hashlib.sha1()
fp1=open('shattered-1.pdf','rb')
fp2=open('shattered-2.pdf','rb')
bad1=fp1.read(320)
bad2=fp2.read(320)
p=remote('66.172.27.77',52317)
r=p.recv()
print zlib.decompress(r)
p.send(zlib.compress('Y'))
r=p.recv()
print zlib.decompress(r)
r=p.recv()
string=zlib.decompress(r)
required=(string.split('\n'))[0][-5:]
for i in xrange(10000000):
#for i in xrange(100):
	suffix=str(hex(i))[2:]
	if len(suffix)%2==1:
		suffix='0'+suffix
	m=hashlib.sha1()
	m.update(bad1+suffix.decode("hex"))
	if m.hexdigest().startswith(required):
		break
p.send(zlib.compress(bad1+suffix.decode("hex")))
r=p.recv()
print zlib.decompress(r)
p.send(zlib.compress(bad2+suffix.decode("hex")))
r=p.recv()
print zlib.decompress(r)
```
Run it and the server would pop the flag.

![Alt flag](./images/flag.png?raw=true)
