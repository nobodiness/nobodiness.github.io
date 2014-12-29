Title: Pipeline与函数式编程
Date: 2014-12-27 2:23
Category: Python
Tags: Pipe
Author: 阿七
Summary: Pipe语法

```python
>>> from pipe import *  
>>> [1, 2, 3, 4, 5] | add  
15  
>>> [5, 4, 3, 2, 1] | sort  
[1, 2, 3, 4, 5]  
```
接下来我们展示一下组合两个或更多的 pipeable 函数：

```python
>>> [1, 2, 3, 4, 5] | where(lambda x: x % 2) | concat  
'1, 3, 5'  
>>> [1, 2, 3, 4, 5] | where(lambda x: x % 2) | tail(2) | concat  
'3, 5'  
>>> [1, 2, 3, 4, 5] | where(lambda x: x % 2) | tail(2) | select(lambda x: x * x) | concat  
'9, 25'  
>>> [1, 2, 3, 4, 5] | where(lambda x: x % 2) | tail(2) | select(lambda x: x * x) | add  
34  
```
因为 Pipe 是惰性求值的，所以我们完成可以弄一个无穷生成器而不用担心内存用完，比如：
```python
>>> def fib():  
...    a, b = 0, 1  
...    while True:  
...        yield a  
...        a, b = b, a + b  
```
求偶数和需要使用到where，作用类似于内建函数filter，过滤出符合条件的元素：

```python
>>> range(5) | where(lambda x: x % 2 == 0) | add
6
```
求出斐波那契数列中所有小于10000的偶数和需要用到take_while，与itertools的同名函数有类似的功能，截取元素直到条件不成立：

```python
>>> fib = fibonacci
>>> fib() | where(lambda x: x % 2 == 0)\
...       | take_while(lambda x: x < 10000)\
...       | add
3382
```
需要对元素应用某个函数可以使用select，作用类似于内建函数map；需要得到一个列表，可以使用as_list：

```python
>>> fib() | select(lambda x: x ** 2) | take_while(lambda x: x < 100) | as_list
[1, 1, 4, 9, 25, 64]
```
pipe中还包括了更多的流处理函数。

你甚至可以自己定义流处理函数，只需要定义一个生成器函数并加上修饰器Pipe。如下定义了一个获取元素直到索引不符合条件的流处理函数：

```python
>>> @Pipe
... def take_while_idx(iterable, predicate):
...   for idx, x in enumerate(iterable):
...     if predicate(idx): yield x
...     else: return
...
```
使用这个流处理函数获取fib的前10个数字：
```python
>>> fib() | take_while_idx(lambda x: x < 10) | as_list
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```
## 一道面试题
读取文件，统计文件中每个单词出现的次数，然后按照次数高低排序。

本来蛮平淡无奇的一题，但一跟前天介绍的 Pipe 结合起来，就有意思了，这类数据流的处理，相当适合用 Pipe 来处理，花了点时间，写代码如下：

```python
from __future__ import print_function  
from re import split  
from pipe import *  
with open('test_descriptor.py') as f:  
  print(f.read()  
        | Pipe(lambda x:split('/W+', x))  
        | Pipe(lambda x:(i for i in x if i.strip()))  
        | groupby(lambda x:x)  
        | select(lambda x:(x[0], (x[1] | count)))  
        | sort(key=lambda x:x[1], reverse=True)  
        )  
 ```

输出：

```python
[('self', 13), ('foo', 9), ('item', 9), ('_data', 8), ('print', 7), ('def', 5), ('return', 5), ('Jeff', 4)]
```
在使用 Pipe 解题的过程中，发现一个问题： 当出错的时候，想找到错误原因太难了！

#### 学习资料
[官方页面](https://github.com/JulienPalard/Pipe)
[Python函数式编程指南（四）：生成器](http://www.cnblogs.com/huxi/archive/2011/07/14/2106863.html)
[Python函数式编程](http://www.jackyshen.com/2014/10/02/functional-programming-in-Python/)
[Pipe——Python 的中缀语法库](http://blog.csdn.net/gzlaiyonghao/article/details/6287114)
[用 Pipe 搞定单词统计的面试题](http://blog.csdn.net/gzlaiyonghao/article/details/6291668)
