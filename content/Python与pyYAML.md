Title: Python与pyYAML
Date: 2014-12-27 13:23
Category: Python
Tags: YAML,pyYAML
Author: 阿七
Summary: YAML

## Import
```python
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
```
```python
import yaml
```
## Loading YAML
```python
>>> yaml.load("""
... - Hesperiidae
... - Papilionidae
... - Apatelodidae
... - Epiplemidae
... """)

['Hesperiidae', 'Papilionidae', 'Apatelodidae', 'Epiplemidae']
```
### utf-8 
```python
>>> yaml.load(u"""
... hello: Привет!
... """)    # In Python 3, do not use the 'u' prefix

{'hello': u'\u041f\u0440\u0438\u0432\u0435\u0442!'}

>>> stream = file('document.yaml', 'r')    # 'document.yaml' contains a single YAML document.
>>> yaml.load(stream)
[...]    # A Python object corresponding to the document.
```
If a string or a file contains several documents, you may load them all with the yaml.load_all function.
```python
>>> for data in yaml.load_all(documents):
...     print data
```
### Object
Even instances of Python classes can be constructed using the !!python/object tag.
```python
>>> class Hero:
...     def __init__(self, name, hp, sp):
...         self.name = name
...         self.hp = hp
...         self.sp = sp
...     def __repr__(self):
...         return "%s(name=%r, hp=%r, sp=%r)" % (
...             self.__class__.__name__, self.name, self.hp, self.sp)

>>> yaml.load("""
... !!python/object:__main__.Hero
... name: Welthyr Syxgon
... hp: 1200
... sp: 0
... """)

Hero(name='Welthyr Syxgon', hp=1200, sp=0)
```
Note that the ability to construct an arbitrary Python object may be dangerous if you receive a YAML document from an untrusted source such as the Internet. The function `yaml.safe_load` limits this ability to simple Python objects like integers or lists.
## Dumping YAML
```python
>>> print yaml.dump({'name': 'Silenthand Olleander', 'race': 'Human',
... 'traits': ['ONE_HAND', 'ONE_EYE']})

name: Silenthand Olleander
race: Human
traits: [ONE_HAND, ONE_EYE]
```
### File
```python
>>> stream = file('document.yaml', 'w')
>>> yaml.dump(data, stream)    # Write a YAML representation of data to 'document.yaml'.
>>> print yaml.dump(data)      # Output the document to the screen.
```
## Constructors, representers, resolvers
### uses metaclass
You may define your own application-specific tags. The easiest way to do it is to define a subclass of yaml.YAMLObject:
```python
>>> class Monster(yaml.YAMLObject):
...     yaml_tag = u'!Monster'
...     def __init__(self, name, hp, ac, attacks):
...         self.name = name
...         self.hp = hp
...         self.ac = ac
...         self.attacks = attacks
...     def __repr__(self):
...         return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
...             self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)
```
The above definition is enough to automatically load and dump Monster objects:
```python
>>> yaml.load("""
... --- !Monster
... name: Cave spider
... hp: [2,6]    # 2d6
... ac: 16
... attacks: [BITE, HURT]
... """)

Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])

>>> print yaml.dump(Monster(
...     name='Cave lizard', hp=[3,6], ac=16, attacks=['BITE','HURT']))

!Monster
ac: 16
attacks: [BITE, HURT]
hp: [3, 6]
name: Cave lizard
```
yaml.YAMLObject uses metaclass magic to register a constructor, which transforms a YAML node to a class instance, and a representer, which serializes a class instance to a YAML node.

### Dice
```python
>>> class Dice(tuple):
...     def __new__(cls, a, b):
...         return tuple.__new__(cls, [a, b])
...     def __repr__(self):
...         return "Dice(%s,%s)" % self

>>> print Dice(3,6)
Dice(3,6)
```
The default representation for Dice objects is not pretty:
```python
>>> print yaml.dump(Dice(3,6))

!!python/object/new:__main__.Dice
- !!python/tuple [3, 6]
```
Suppose you want a Dice object to represented as AdB in YAML:
```python
>>> print yaml.dump(Dice(3,6))

3d6
```
### representer
First we define a representer that converts a dice object to a scalar node with the tag !dice, then we register it.
```python
>>> def dice_representer(dumper, data):
...     return dumper.represent_scalar(u'!dice', u'%sd%s' % data)

>>> yaml.add_representer(Dice, dice_representer)
Now you may dump an instance of the Dice object:

>>> print yaml.dump({'gold': Dice(10,6)})
{gold: !dice '10d6'}
```
### constructor
Let us add the code to construct a Dice object:
```python
>>> def dice_constructor(loader, node):
...     value = loader.construct_scalar(node)
...     a, b = map(int, value.split('d'))
...     return Dice(a, b)

>>> yaml.add_constructor(u'!dice', dice_constructor)
```
Then you may load a Dice object as well:
```python
>>> print yaml.load("""
... initial hit points: !dice 8d4
... """)

{'initial hit points': Dice(8,4)}
```
### without `!dice`
You might not want to specify the tag !dice everywhere. There is a way to teach PyYAML that any untagged plain scalar which looks like XdY has the implicit tag !dice. Use add_implicit_resolver:
```python
>>> import re
>>> pattern = re.compile(r'^\d+d\d+$')
>>> yaml.add_implicit_resolver(u'!dice', pattern)
Now you don't have to specify the tag to define a Dice object:

>>> print yaml.dump({'treasure': Dice(10,20)})

{treasure: 10d20}

>>> print yaml.load("""
... damage: 5d10
... """)

{'damage': Dice(5,10)}
```

## [数据类型(Tags)](http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLtagsandPythontypes)
YAML tags and Python types

The following table describes how nodes with different tags are converted to Python objects.

YAML tag  |  Python type
----------|--------------
**Standard YAML tags**   
!!null          | None
!!bool          | bool
!!int           | int or long (int in Python 3)
!!float         | float
!!binary        |  str (bytes in Python 3)
!!timestamp     | datetime.datetime
!!omap, !!pairs | list of pairs
!!set           | set
!!str           | str or unicode (str in Python 3)
!!seq           | list
!!map           | dict
**Python-specific tags**  
!!python/none     | None
!!python/bool     | bool
!!python/bytes    | (bytes in Python 3)
!!python/str      | str (str in Python 3)
!!python/unicode  |  unicode (str in Python 3)
!!python/int      |  int
!!python/long     | long (int in Python 3)
!!python/float    | float
!!python/complex  |  complex
!!python/list     | list
!!python/tuple    | tuple
!!python/dict     | dict
**Complex Python tags**
!!python/name:module.name      |  module.name
!!python/module:package.module |  package.module
!!python/object:module.cls     | module.cls instance
!!python/object/new:module.cls | module.cls instance
!!python/object/apply:module.f | value of f(...)

## [API] (http://pyyaml.org/wiki/PyYAMLDocumentation#Reference)

#### 学习资料:
[官方文档](http://pyyaml.org/wiki/PyYAMLDocumentation)
