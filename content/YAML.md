Title: YAML
Date: 2014-12-27 3:23
Category: Python
Tags: YAML
Author: 阿七
Summary: YAML的语法介绍

## 注释
```yaml
# Comment Example
```
## 文档
使用`---`分隔文档
```yaml
# documents example
---
- Ada
- APL
- ASP

- Assembly
- Awk
---
- Basic
---
- C
- C#    # Note that comments are denoted with ' #' (space then #).
- C++
- Cold Fusion
```

## 数据结构
YAML的设计者认为在配置文件中所要表达的数据内容有三种类型：标量(Scalar，如字符串和整数等)、序列（Sequence，如数组）和Mapping（类似hash的key/value pair）。
### 标量
There are 5 styles of scalars in YAML: plain, single-quoted, double-quoted, literal, and folded:
```yaml
# YAML
plain: Scroll of Remove Curse
single-quoted: 'EASY_KNOW'
double-quoted: "?"
literal: |    # Borrowed from http://www.kersbergen.com/flump/religion.html
  by hjw              ___
     __              /.-.\
    /  )_____________\\  Y
   /_ /=== == === === =\ _\_
  ( /)=== == === === == Y   \
   `-------------------(  o  )
                        \___/
folded: >
  It removes all ordinary curses from all equipped items.
  Heavy or permanent curses are unaffected.
```
```python
# Python
{'plain': 'Scroll of Remove Curse',
'literal':
    'by hjw              ___\n'
    '   __              /.-.\\\n'
    '  /  )_____________\\\\  Y\n'
    ' /_ /=== == === === =\\ _\\_\n'
    '( /)=== == === === == Y   \\\n'
    ' `-------------------(  o  )\n'
    '                      \\___/\n',
'single-quoted': 'EASY_KNOW',
'double-quoted': '?',
'folded': 'It removes all ordinary curses from all equipped items. Heavy or permanent curses are unaffected.\n'}
```
Each style has its own quirks. A plain scalar does not use indicators to denote its start and end, therefore it's the most restricted style. Its natural applications are names of attributes and parameters.

Using single-quoted scalars, you may express any value that does not contain special characters. No escaping occurs for single quoted scalars except that a pair of adjacent quotes '' is replaced with a lone single quote '.

Double-quoted is the most powerful style and the only style that can express any scalar value. Double-quoted scalars allow escaping. Using escaping sequences \x** and \u****, you may express any ASCII or Unicode character.

There are two kind of block scalar styles: literal and folded. The literal style is the most suitable style for large block of text such as source code. The folded style is similar to the literal style, but two adjacent non-empty lines are joined to a single line separated by a space character.
### 序列(Block)
```yaml
# YAML
-
  - HTML
  - LaTeX
  - SGML
  - VRML
  - XML
  - YAML
-
  - BSD
  - GNU Hurd
  - Linux
```
```python
# Python
[['HTML', 'LaTeX', 'SGML', 'VRML', 'XML', 'YAML'], ['BSD', 'GNU Hurd', 'Linux']]
```

### 字典(Block)
```yaml
# YAML
base armor class: 0
base damage: [4,4]
plus to-hit: 12
plus to-dam: 16
plus to-ac: 0
```
```python
# Python
{'plus to-hit': 12, 'base damage': [4, 4], 'base armor class': 0, 'plus to-ac': 0, 'plus to-dam': 16}
```
Complex keys are denoted with ? (question mark then space):
```yaml
# YAML
? !!python/tuple [0,0]
: The Hero
? !!python/tuple [0,1]
: Treasure
? !!python/tuple [1,0]
: Treasure
? !!python/tuple [1,1]
: The Dragon
```
```python
# Python
{(0, 1): 'Treasure', (1, 0): 'Treasure', (0, 0): 'The Hero', (1, 1): 'The Dragon'}
```
### Flow collections
```yaml
# YAML
{ str: [15, 17], con: [16, 16], dex: [17, 18], wis: [16, 16], int: [10, 13], chr: [5, 8] }
```
```python
# Python
{'dex': [17, 18], 'int': [10, 13], 'chr': [5, 8], 'wis': [16, 16], 'str': [15, 17], 'con': [16, 16]}
```
## 别名(Aliases)
Using YAML you may represent objects of arbitrary graph-like structures. If you want to refer to the same object from different parts of a document, you need to use anchors and aliases.

Anchors are denoted by the `&` indicator while aliases are denoted by `*`. For instance, the document
```yaml
left hand: &A
  name: The Bastard Sword of Eowyn
  weight: 30
right hand: *A
```
expresses the idea of a hero holding a heavy sword in both hands.

PyYAML now fully supports recursive objects. For instance, the document
```yaml
&A [ *A ]
```
will produce a list object containing a reference to itself.

#### 学习资料:
[初探YAML](http://www.cnblogs.com/chwkai/archive/2009/03/01/249924.html)
[官方文档](http://pyyaml.org/wiki/PyYAMLDocumentation)
[YAML Reference card](http://www.yaml.org/refcard.html)
[YAML -- 想要爱你很容易](http://www.ibm.com/developerworks/cn/xml/x-1103linrr/)

