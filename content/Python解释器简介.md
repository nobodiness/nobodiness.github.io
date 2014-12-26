Title: Python解释器简介
Date: 2014-12-27 1:26
Category: Python
Tags: 解释器
Author: 阿七
Summary: Python字节码初步的学习笔记

Python解释器简介


## 函数对象
```python
>>> def foo(a):
...     x = 3
...     return x + a
...
>>> foo
<function foo at 0x107ef7aa0>
```
Python中的函数是一个对象
## 代码对象
函数的func_code属性就是代码对象
```python
>>> def foo(a):
...     x = 3
...     return x + a
...
>>> foo
<function foo at 0x107ef7aa0>
>>> foo.func_code
<code object foo at 0x107eeccb0, file "<stdin>", line 1>
```
我们只关注3个有趣的 foo 函数代码对象的属性。
```python
>>> foo.func_code.co_varnames
('a', 'x')
>>> foo.func_code.co_consts
(None, 3)
>>> foo.func_code.co_argcount
1
```
通过调用它们，我们能依次得到：**变量名**、**函数中已知的常量**和**函数参数的数量**。但是目前为止，我们还是不知道生成代码对象的指令到底是什么。事实上，这个指令叫做字节码。字节码也是代码对象的一个属性：
```python
>>> foo.func_code.co_code
'd\x01\x00}\x01\x00|\x01\x00|\x00\x00\x17S'
```
## 字节码

那么什么是字节码呢？其实，它就是一系列的字节。这些字节打印出来的样子很奇怪是因为有些字节是能够打印的而有些不能。从分析ord的每个字节中我们看到它们只是数字而已。
```python
>>> [ord(b) for b in foo.func_code.co_code]
[100, 1, 0, 125, 1, 0, 124, 1, 0, 124, 0, 0, 23, 83]
```
这就是那些组成python字节码的字节。解释器会循环接收各个字节，查找每个字节的指令然后执行这个指令。需要注意的是，字节码本身并不包括任何python对象,或引用任何对象。

如果你想知道python字节码的意思，可以去找到CPython解释器文件(ceval.c)，然后查阅100的意思、1的意思、0的意思，等等。在后续内容中，我们会这么做的！但暂时可以用更简单的方法： `dis 模块`。

## 反汇编字节码

反汇编字节码的意思就是接收这一系列的字节，然后打印出我们能够理解的字符。这并不是python的工作; `dis `模块只是帮助我们了解python内部工作的中间状态。我不支持在产品代码中使用 `dis` ——它是面向程序员的，不是电脑。

但是，现在我们需要做的正是让一些字节码变得更通俗易懂，所以 `dis` 是一个非常理想的工具。我们将使用 `dis.dis` 函数去分析 `foo` 函数的代码对象。

```python
>>> def foo(a):
...     x = 3
...     return x + a
...
>>> import dis
>>> dis.dis(foo.func_code)
  2           0 LOAD_CONST               1 (3)
              3 STORE_FAST               1 (x)
 
  3           6 LOAD_FAST                1 (x)
              9 LOAD_FAST                0 (a)
             12 BINARY_ADD
             13 RETURN_VALUE
```
（你通常会看到这种写法：`dis.dis(foo)`,直接分析它的函数对象。这其实是一种简便写法： `dis` 真正分析的还是代码对象。如果要传递一个函数，那么只能接收到它的代码对象。）

左边那一列数字是原始源代码的行号。第二列是字节码的偏移量：`LOAD_CONST`在第0行，`STORE_FAST`在第3行，以此类推。中间那列是字节的名字。它们是为程序员所准备的——解释器是完全不需要的。

最后两列告诉我们一些关于指令参数（如果有的话）的细节。第四列是参数本身。它表示一个指向代码对象其它属性的索引。在这个例子中，`LOAD_CONST`的参数指向列表`co_consts`，`STORE_FAST`的参数指向`co_varnames`。`dis`在第四列所指向的的地方查找常数或者名称, 最后在第五列返回给我们它找到的数据。这很容易就能得到证实了：

```python
>>> foo.func_code.co_consts[1]
3
>>> foo.func_code.co_varnames[1]
'x'
```
这也能解释为什么第二个指令`STORE_FAST`位于字节码的第三行。如果一个字节码有参数的话，那么它相邻的两个字节的参数和它相同。当然，正确的处理这些数据是解释器的工作。

#### 未完
[第四节](http://blog.jobbole.com/57381/)

#### 学习资料
精简自:[Python解释器简介](http://blog.jobbole.com/55327/)
