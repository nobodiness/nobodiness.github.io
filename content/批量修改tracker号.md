Title: 批量修改tracker号
Date: 2014-12-20 12:47
Category: Python
Tags: 小程序,md5,bt,bencode
Author: 阿七
Summary: 修改tracker方便上传百度云

百度云bt下载是个好东西,可是我的种子一般从pt站中得到,直接上传百度云下载会被封号.

从pt站下载的种子,修改tracker再上传就没有问题了

以下是一个批量转换整个目录中所有种子文件tracker的python代码
留在这里做个备份

## 用到的库
+ [bencode](https://pypi.python.org/pypi/bencode/1.0)
一个种子解析的第三方库(需要`pip install`,你懂得)
是有人从BitTorrent客户端(Python写的)中截出来的
+ [hashlib](https://docs.python.org/2/library/hashlib.html)
hash加密库,可以加解密md5,和sha
这里配合`random`用来产生逼真的md5码

## 用法
### bencode
```python
# 解码
decode = bdecode(f.read())
# 编码
f.write(bencode(decode))
```
### hashlib
##### 从[这里](http://blog.csdn.net/jgood/article/details/4276398)抄一段:

使用Python中的hashlib来进行hash加密是非学简单的，下面是一段简单代码：
```python
import hashlib  
md5 = hashlib.md5() #创建一个MD5加密对象  
md5.update("JGood is a handsome boy")  #更新要加密的数据  
print md5.digest()  #加密后的结果（二进制）  
print md5.hexdigest() #加密后的结果，用十六进制字符串表示。  
print 'block_size:', md5.block_size  
print 'digest_size:', md5.digest_size  
```
非常的简单，其实如果说加密一个字符串，根本不用写上面这么多代码，一条语句就可以了：
```python
print '-' * 25, '更简洁的语法', '-' * 25  
print hashlib.new("md5", "JGood is a handsome boy").hexdigest()  
```

##### [官方](https://docs.python.org/2/library/hashlib.html)的例子
For example, to obtain the digest of the string 'Nobody inspects the spammish repetition':
```python
>>> import hashlib
>>> m = hashlib.md5()
>>> m.update("Nobody inspects")
>>> m.update(" the spammish repetition")
>>> m.digest()
'\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'
>>> m.digest_size
16
>>> m.block_size
64
```
Using new() with an algorithm provided by OpenSSL:
```python
>>> h = hashlib.new('ripemd160')
>>> h.update("Nobody inspects the spammish repetition")
>>> h.hexdigest()
'cc4a5ce1b3df48aec5d22d1f16b894a0b894eccc'
```
### 文件操作
`.`目录下所有的torrent文件
```python
[x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.torrent']
```
一句话体现python的简洁优美

重命名
```python
os.rename(filename,newname)
```


#### 以下是完整的代码:
```python
import os
import hashlib
import random
from bencode import *

def randmd5():
    rstring = ''.join(random.sample(str(range(1,100)),30))
    return hashlib.new("md5", rstring).hexdigest()

filelist = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.torrent']
for filename in filelist:
    with open(filename,'r+b') as f:
        decode = bdecode(f.read())
        print decode['announce']
        decode['announce'] = 'https://tp.x-xxxx.xx/announce.php?passkey=%s'%randmd5()
        print decode['announce']
        f.seek(0)
        f.write(bencode(decode))
    os.rename(filename,decode['info']['name']+".torrent")
```
