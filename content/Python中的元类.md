Title: Python中的元类
Date: 2014-12-26 13:56
Category: Python
Tags: 面向对象,元类
Author: 阿七
Summary: Python元类笔记
Status: draft


## 动态创建类 type()

type()函数既可以返回一个对象的类型，又可以创建出新的类型，比如，我们可以通过type()函数创建出Hello类，而无需通过class Hello(object)...的定义：

```python
>>> def fn(self, name='world'): # 先定义函数
...     print('Hello, %s.' % name)
...
>>> Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
>>> h = Hello()
>>> h.hello()
Hello, world.
>>> print(type(Hello))
<type 'type'>
>>> print(type(h))
<class '__main__.Hello'>
Try
```

要创建一个class对象，type()函数依次传入3个参数：**class的名称****继承的父类集合**，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法**class的方法名称与函数绑定**，这里我们把函数fn绑定到方法名hello上。

通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。 

## 元类 metaclass

#### 学习文献
[Python 中的元类编程](https://www.ibm.com/developerworks/cn/linux/l-pymeta/)
[五分钟理解元类（Metaclasses）](http://blog.csdn.net/gzlaiyonghao/article/details/3048947)
[廖雪峰-使用元类](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820064557c69858840b4c48d2b8411bc2ea9099ba000)
[深刻理解Python中的元类(metaclass)](http://blog.jobbole.com/21351/)
