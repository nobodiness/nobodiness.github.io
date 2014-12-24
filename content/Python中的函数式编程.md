Title: Python中的函数式编程
Date: 2014-12-23 17:25
Category: Python
Tags: 函数式编程
Author: 阿七
Summary: Python函数式编程笔记

在开始设计模式的学习之前,我感到有必要先复习一下Python中的函数式编程和面向对象.

## 高阶函数
以函数为参数的函数
```python
def add(x, y, f):
    return f(x) + f(y)
```
```python
>>> add(-5, 6, abs)
11
```
## map filter

`map` 和 `filter` 在 python 中都有列表推导的实现

这个例子:
```python
>>> def f(x):
...     return x * x
...
>>> map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
[1, 4, 9, 16, 25, 36, 49, 64, 81]
```
等同于
```python
[x * x for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]]
```
这个例子:
```python
>>> def is_odd(n):
...     return n % 2 == 1
>>> filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])
[1, 5, 9, 15]
```
等同于
```python
[x for x in [1, 2, 4, 5, 6, 9, 10, 15] if x % 2 == 1]
```

map reduce还是实现并行化的神器
可以看看这篇文[Python 并行任务技巧](http://segmentfault.com/a/1190000000382873)

## Reduce与部分内建函数介绍
`reduce` 在 python3 中被移除了,因为创始人觉得他太让人费解
```python
all(iterable) == reduce(lambda x, y: bool(x and y), iterable)
any(iterable) == reduce(lambda x, y: bool(x or y), iterable)
max(iterable[, args...][, key]) \
    == reduce(lambda x, y: x if key(x) > key(y) else y, iterable_and_args)
min(iterable[, args...][, key]) \
    == reduce(lambda x, y: x if key(x) < key(y) else y, iterable_and_args)
sum(iterable[, start]) == reduce(lambda x, y: x + y, iterable, start)
map(function, iterable, ...)
```

`zip(iterable1, iterable2, ...)` 这个函数返回一个列表，每个元素都是一个元组. 
例如：`zip([1, 2], [3, 4])` --> `[(1, 3), (2, 4)]` 如果参数的长度不一致，将在最短的序列结束时结束；如果不提供参数，将返回空列表。

## 排序

一个字符串排序的例子：
```python
>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
['Credit', 'Zoo', 'about', 'bob']
```
默认情况下，对字符串排序，是按照ASCII的大小比较的，由于'Z' < 'a'，结果，大写字母Z会排在小写字母a的前面。

现在，我们提出排序应该忽略大小写，按照字母序排序。要实现这个算法，不必对现有代码大加改动，只要我们能定义出忽略大小写的比较算法就可以：
```python
def cmp_ignore_case(s1, s2):
    u1 = s1.upper()
    u2 = s2.upper()
    if u1 < u2:
        return -1
    if u1 > u2:
        return 1
    return 0
```
忽略大小写来比较两个字符串，实际上就是先把字符串都变成大写（或者都变成小写），再比较。

这样，我们给sorted传入上述比较函数，即可实现忽略大小写的排序：
```python
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)
['about', 'bob', 'Credit', 'Zoo']
```
## 匿名函数
```python
>>> map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])
[1, 4, 9, 16, 25, 36, 49, 64, 81]
```
匿名函数还可以作为返回值
```python
def build(x, y):
    return lambda: x * x + y * y
```
## 偏函数
偏函数的作用就是，把一个函数的某些参数（不管有没有默认值）给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。 
```python
>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85
```
注意到上面的新的int2函数，仅仅是把base参数重新设定默认值为2，但也可以在函数调用时传入其他值.

## 装饰器

### 不含参装饰器

```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        return func(*args, **kw)
    return wrapper
@log
def now():
    print '2013-12-25'
```

装饰器相当于`now = log(now)`
`@functools.wraps(func)`相当于`wrapper.__name__ = func.__name__`

```python
>>> now()
call now():
2013-12-25
```

### 含参装饰器

```python
import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now():
    print '2013-12-25'
```

相当于`now = log('execute')(now)`

```python
>>> now()
execute now():
2013-12-25
```
### 内置的装饰器

内置的装饰器有三个，分别是`staticmethod`、`classmethod`和`property`，作用分别是把类中定义的实例方法变成静态方法、类方法和类属性。由于模块里可以定义函数，所以静态方法和类方法的用处并不是太多，除非你想要完全的面向对象编程。而属性也不是不可或缺的，Java没有属性也一样活得很滋润。从我个人的Python经验来看，我没有使用过`property`，使用`staticmethod`和`classmethod`的频率也非常低。

注: **静态方法**：无法访问类属性、实例属性，相当于一个相对独立的方法，跟类其实没什么关系，换个角度来讲，其实就是放在一个类的作用域里的函数而已。
**类方法**：可以访问类属性，无法访问实例属性。

```python
class Rabbit(object):

    def __init__(self, name):
        self._name = name

    @staticmethod
    def newRabbit(name):
        return Rabbit(name)

    @classmethod
    def newRabbit2(cls):
        return Rabbit('')

    @property
    def name(self):
        return self._name
```

这里定义的属性是一个只读属性，如果需要可写，则需要再定义一个setter：

```python
@name.setter
def name(self, name):
    self._name = name
```
关于`@property`在下一篇Python中的面向对象中详细说明

### 装饰器用于程序分析
时间分析: [line_profiler](http://packages.python.org/line_profiler/)
内存分析: [memory_profiler](https://github.com/fabianp/memory_profiler)
使用方法见文章 [Python程序的性能分析指南](http://blog.jobbole.com/47619/)


#### 学习文章
[廖雪峰-函数式编程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386819866394c3f9efcd1a454b2a8c57933e976445c0000)
[Python函数式编程指南（二）：函数](http://www.cnblogs.com/huxi/archive/2011/06/24/2089358.html)
[Python程序的性能分析指南](http://blog.jobbole.com/47619/)





