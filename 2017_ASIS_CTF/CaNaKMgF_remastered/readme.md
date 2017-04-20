# Writeup

## 1. Binary Analysis

First thing first,**checksec**.

```
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

The differences between original challenge CaNaKMgF are **PIE is ENABLED and RELRO is FULL**.

Also the arbitrary file read in original CaNaKMgF has been replaced with an exit(0).

The major vulnerability is **Dangling pointer**。

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/1.jpg)

## 2.Exploit

### 2.1 Leak
Since we cannot read /proc/self/maps to defeat ASLR,there must be another way.

After the smallbin is freed, there will be a pointer stores at the first QWORD value in this memory.

Function do_read doesn't check if the pointer is freed(In fact this is unable to check), so there are 3 steps to leak libc.

> * malloc a smallbin
> * free this smallbin
> * read the smallbin

Now we have base address of libc, let's play with fastbin!.

### 2.2 Fastbin Attack

This will tricks malloc into returning a nearly-arbitrary pointer by abusing the fastbin freelist.

General process splits in some steps.

> 1. malloc 3 fastbins in exactly same size.
> 2. free the first fastbin.
> 3. free the second fastbin.
> 4. free the first fastbin again!
> 5. malloc a fastbin with same size used before.
> 6. edit the first QWORD in memory just returned (freelist's FD pointer) to an arbitrary pointer.
> 7. malloc second fastbin with same size.
> 8. malloc third fastbin with same size.
> 9. now the arbitrary pointer should be in fastbin freelist!
> 10. another malloc will return the arbitrary porint we just write in step 6!

But this trick returns nearly-arbitrary pointer ,because there should be a corresponding size stores in next QWORD of the pointer you want.

Last time I chose the memory right before the malloc_hook, this time I chose a memory inside stdout in libc.

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/2.jpg)

Yes! memory chunk doesn't need to be aligned!

And 0x7f matches the size 0x70 in fastbin!

Now we can trick malloc to reurn a pointer inside the stdout,cool!

Next we can modify the pointer of vtable, btw the libc version is 2.23 and it doesn't contain a vtable check!

While the puts in print_menu function is called, we will control the rip by modifying vtable in stdout,but this is a one-shoot jump.

First I consider the magic gadgets in libc,but sadly none of this gadgets works.

I suddenly noticed that while we control the rip,the rdi points to stdout pointer!

Why not just control rip to **function gets**?

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/3.jpg)

Now we can modify the whole content of stdout!

-- How to spawn a shell?

-- system("/bin/sh") !

This time we will overwrite the vtable like this:

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/4.jpg)

This will call system('1\x80;/bin/sh;') after next puts called!

What '1\x80;' does here?

Let's see the implementation of puts.

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/5.jpg)

so just put a \x80 there :)

All done! we have a shell!!

![alt](https://raw.githubusercontent.com/Kung-Pao-Chicken/ctf/master/2017_ASIS_CTF/CaNaKMgF_remastered/6.jpg)
