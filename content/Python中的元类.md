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
```

要创建一个class对象，type()函数依次传入3个参数：**class的名称** **继承的父类集合**，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法**class的方法名称与函数绑定**，这里我们把函数fn绑定到方法名hello上。

通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。 

## new 模块中的类工厂
new 模块与上面相同
```python
>>> from new import classobj
>>> Foo2 = classobj('Foo2',(Foo,),{'bar':lambda self:'bar'})
>>> Foo2().bar()
'bar'
>>> Foo2().say_foo()
foo
```

## 元类 metaclass
元类就是用来创建类的“东西”。你创建类就是为了创建类的实例对象，不是吗？但是我们已经学习到了Python中的类也是对象。好吧，元类就是用来创建这些类（对象）的，元类就是类的类，你可以这样理解为：

```python
MyClass = MetaClass()
MyObject = MyClass()
```
你已经看到了type可以让你像这样做：

```python
MyClass = type('MyClass', (), {})
```
这是因为函数`type`实际上是一个元类。`type`就是Python在背后用来创建所有类的元类。现在你想知道那为什么`type`会全部采用小写形式而不是`Type`呢？好吧，我猜这是为了和`str`保持一致性，`str`是用来创建字符串对象的类，而`int`是用来创建整数对象的类。`type`就是创建类对象的类。你可以通过检查`__class__`属性来看到这一点。Python中所有的东西，注意，我是指所有的东西——都是对象。这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。

```python
>>> age = 35
>>> age.__class__
<type 'int'>
>>> name = 'bob'
>>> name.__class__
<type 'str'>
>>> def foo(): pass
>>>foo.__class__
<type 'function'>
>>> class Bar(object): pass
>>> b = Bar()
>>> b.__class__
<class '__main__.Bar'>
```
现在，对于任何一个`__class__`的`__class__`属性又是什么呢？

```python
>>> a.__class__.__class__
<type 'type'>
>>> age.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> b.__class__.__class__
<type 'type'>
```
因此，元类就是创建类这种对象的东西。如果你喜欢的话，可以把元类称为“类工厂”（不要和工厂类搞混了:D） type就是Python的内建元类，当然了，你也可以创建自己的元类。


#### 学习文献
推荐:[深刻理解Python中的元类(metaclass)](http://blog.jobbole.com/21351/)

[Python 中的元类编程](https://www.ibm.com/developerworks/cn/linux/l-pymeta/)
[五分钟理解元类（Metaclasses）](http://blog.csdn.net/gzlaiyonghao/article/details/3048947)
[廖雪峰-使用元类](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820064557c69858840b4c48d2b8411bc2ea9099ba000)

