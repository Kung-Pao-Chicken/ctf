
这题给了四个文件，specialRSA.py可以把msg.txt加密成msg.enc，需要分析过程把flag.enc解密出来。    当时没去做这题是事后看writeup的。  
https://cryptsec.wordpress.com/2016/03/21/bctf-2016-write-up-special-rsa-crypto-200/ http://ddaa.tw/bctf_crypto_200_special_rsa.html  
脚本里面连解密算法都给了，只是基数k不知道，所以需要先求k。那怎么求呢？  
第一篇wr里那张图解释得挺好。  
看完图后仍然懵逼了两下：  
一个是不明白哪来的m1,m2,c1,c2，给的密文不是只有一个msg.enc，明文只有一个msg.txt吗？  其实是加密的时候会把它切成256字符长的段。明文直接切，密文用msgpack去unpack一下就有。  
二是不明白图中c1为什么可以整除m1。  
后来反应过来那他妈是模逆运算，不是真的除啊= =。  
然后就能看懂了。。台湾组写的比较详细，可以复习一下遗忘的RSA知识  
1.%运算优先度最低  
2.满足加法律：a + b % N = (a % N + b % N) % N   
3.满足减法律：a - b % N = (a % N - b % N) % N  
4.满足乘法律：a * b % N = (a % N * b % N) % N  
5.满足除法律：a * b_inv % N = (a % N / b % N) % N  
6. 指数等于连乘，因此满足指数律  
*(a * b) ^ r % N = (a ^ r % N) * (b ^ r % N) % N  
*(a - b) ^ r % N = (a ^ r % N) / (b ^ r % N) % N  
*g ^ (a + b) % N = (g ^ a % N) * (g ^ b % N) % N  
7.任何数乘上模反元素，余数会是1  
*a * a_inv % N = 1


  
  
