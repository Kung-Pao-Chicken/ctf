#Stego150_Midifan  
  这题当时也并没有人做。就是那种典型的，看完writeup之后感觉每一步都很简单，但是自己想却不可能想到的题= =  
  
##Step 1. 找原音频  
  首先拿到魂斗罗的主题曲，又没有别的信息肯定会先去找原音轨（因为现在的音轨毋庸置疑是改过的嘛）。  
  百度“魂斗罗 midi”找到无数音频但是听起来都不对，好容易找到一个名字叫midifan的网站，上面有魂斗罗midi主题曲，激动地下下来（因为这个网站的名字跟题目一样啊），打开一看尼玛还是不对，坑！  
  最后我投降看了ppp的wr说要用元数据去搜，果然搜到了= =。唉  
  虽然后来it turns out that原音频没有也可以但是感觉这种题还是会去找的= =。  
  
##Step2. 分析音频  
  用什么软件来分析呢，刚开始受误导去搞了个cakewalk，打开后一脸懵逼看不懂，毕竟人家是专业的音频合成软件，不是数值分析的。  
  师弟说可以把midi转成csv，果然有人做好了工具，完美。  
  
##Step3. 数值分析  
  转成csv之后这题的异常数据还是比较容易发现的，就是那些多出来的1。  
  但还是有两个小坑。  
  一是8bit转1byte很好实现，但是前面多个0少个0结果就完全不一样了，我刚开始多了个0= =。  
  二是这8bit还不能直接转，要先逆序一下。python可以用[::-1]方便地实现。  
  另外就是这题用excel直接把不需要的数据筛掉比代码方便很多。  

python代码  
```
import re
fp1=open('midifan_filtered.csv','r')
fp2=open('calculated.txt','w+')
for line in fp1:
	num=(re.findall('([0-9]+),\sNote',line))[0]
	num=int(num)
	if num%4==0:
		fp2.write('0')
	else:
		fp2.write('1')
fp2.close()
answer=''
fp3=open('calculated.txt','r')
eight=fp3.read(8)
while len(eight)!=0:
	char=int(eight[::-1],2)
	answer+=chr(char)
	eight=fp3.read(8)
fp3.close()
print answer
```