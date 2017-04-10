In this challenge, we are given an ELF-64 file. After making an attempt to run it, we know that correct flag should be given as argv[1].

Then drag it into IDA. Result of static analysis was a real mess because the program was written in C++. However, the position of final comparison was clear, that was on 0x4010a0.

![Alt ida01](./images/ida01.png?raw=true)

Our input string, after certain transformation, should become that shown in picture ("82a38...") to produce a correct result. Not knowing what kind of transformation it is, I set breakpoint on 0x4010a0, to see whether input chars and transformed chars have one-to-one correspondence. Luckily they have.
So I wrote a script with a table that reflect the correspondence relationship. After running it we quickly got the flag.

```
origin="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghkjilmnopqrstuvwxyz1234567890~!@#$%^&*()_{}"
after="828183888a898b848685878c8e8d8fa0a2a1a3a8aaa9aba4a6a5929193989a999b949795969c9e9d9fb0b2b1b3b8bab9bbb4b6b5323133383a393b343630bd128013181aad19151416afb7bf"
answer="82a386a3b7983198313b363293399232349892369a98323692989a313493913036929a303abf"

afterarray=[]
answerarray=[]
for i in range(76):
	afterarray.append(after[i*2:i*2+2])
for i in range(38):
	answerarray.append(answer[i*2:i*2+2])
for onebyte in answerarray:
	print origin[afterarray.index(onebyte)],
```

flag:ASIS{d2d2791c6a18da9ed19ade28cb09ae05}