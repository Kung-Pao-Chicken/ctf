
  这题给了四个文件，specialRSA.py可以把msg.txt加密成msg.enc，需要分析过程把flag.enc解密出来。
  当时没去做这题是事后看writeup的。
https://cryptsec.wordpress.com/2016/03/21/bctf-2016-write-up-special-rsa-crypto-200/
http://ddaa.tw/bctf_crypto_200_special_rsa.html
  脚本里面连解密算法都给了，只是基数k不知道，所以需要先求k。那怎么求呢？
  wr里那张图解释得挺好