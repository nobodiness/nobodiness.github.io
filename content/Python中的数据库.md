Title: Python中的数据库
Date: 2014-12-23 21:25
Category: Python
Tags: 数据库,SQLite
Author: 阿七
Summary: 关于数据库的笔记,数据库以SQLite为例

## 导入Python SQLITE数据库模块

```python
import sqlite3
cx = sqlite3.connect("E:/test.db")
```

## 创建/打开数据库

也可以创建数据库在内存中。

```python
con = sqlite3.connect(":memory:")
```

## 数据库连接对象

打开数据库时返回的对象`cx`就是一个数据库连接对象，它可以有以下操作：

```python
commit()   # 事务提交
rollback() # 事务回滚
close()    # 关闭一个数据库连接
cursor()   # 创建一个游标
```

关于`commit()`，如果`isolation_level`隔离级别默认，那么每次对数据库的操作，都需要使用该命令，你也可以设置`isolation_level = None`，这样就变为自动提交模式。 conn.isolation_level = None #这个就是事务隔离级别，默认是需要自己commit才能修改数据库，置为None则自动每次修改都提交,否则为""

## 使用游标查询数据库

我们需要使用游标对象SQL语句查询数据库，获得查询对象。 通过以下方法来定义一个游标。 游标把作为面向集合的数据库管理系统和面向行的程序设计两者联系起来，使两个数据处理方式能够进行沟通。

```python
cu = cx.cursor()
```

游标对象有以下的操作：

```python
execute()    #执行sql语句
executemany()#执行多条sql语句
close()      #关闭游标
fetchone()   #从结果中取一条记录，并将游标指向下一条记录
fetchmany()  #从结果中取多条记录
fetchall()   #从结果中取出所有记录
scroll()     #游标滚动
```

### 1.建表

```python
cu.execute("create table catalog \
(id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
```

上面语句创建了一个叫catalog的表，它有一个主键id，一个pid，和一个name，name是不可以重复的，以及一个nickname默认为NULL。

### 2.插入数据

请注意避免以下写法：

```python
# Never do this -- insecure 会导致注入攻击

pid=200
c.execute("... where pid = '%s'" % pid)
```

正确的做法如下，如果t只是单个数值，也要采用t=(n,)的形式，因为元组是不可变的。

```python
for t in[(0,10,'abc','Yu'),(1,20,'cba','Xu')]:
    cx.execute("insert into catalog values (?,?,?,?)", t)
```

简单的插入两行数据,不过需要提醒的是,只有提交了之后,才能生效.我们使用数据库连接对象cx来进行提交commit和回滚rollback操作.

```python
cx.commit()
```

### 3.查询

```python
cu.execute("select * from catalog")
```

要提取查询到的数据,使用游标的fetch函数,如:

```
In [10]: cu.fetchall()
Out[10]: [(0, 10, u'abc', u'Yu'), (1, 20, u'cba', u'Xu')]
```

如果我们使用`cu.fetchone()`,则首先返回列表中的第一项,再次使用,则返回第二项,依次下去.

### 4.修改

```
In [12]: cu.execute("update catalog set name='Boy' where id = 0")
In [13]: cx.commit()
```

注意,修改数据以后提交

### 5.删除

```python
cu.execute("delete from catalog where id = 1")
cx.commit()
```

### 6.使用中文

请先确定你的IDE或者系统默认编码是utf-8,并且在中文前加上u

```python
x=u'鱼'
cu.execute("update catalog set name=? where id = 0",x)
cu.execute("select * from catalog")
cu.fetchall()
[(0, 10, u'\u9c7c', u'Yu'), (1, 20, u'cba', u'Xu')]
```

如果要显示出中文字体，那需要依次打印出每个字符串

```
In [26]: for item in cu.fetchall():
   ....:     for element in item:
   ....:         print element,
   ....:     print
   ....:
0 10 鱼 Yu
1 20 cba Xu
```

## API列表

`sqlite3.connect(database [,timeout ,other optional arguments])` 该 API 打开一个到 SQLite 数据库文件 database 的链接。您可以使用 `:memory:` 来在 RAM 中打开一个到 database 的数据库连接，而不是在磁盘上打开。如果数据库成功打开，则返回一个连接对象。

当一个数据库被多个连接访问，且其中一个修改了数据库，此时 SQLite 数据库被锁定，直到事务提交。timeout 参数表示连接等待锁定的持续时间，直到发生异常断开连接。`timeout` 参数默认是 5.0（5 秒）。

如果给定的数据库名称 filename 不存在，则该调用将创建一个数据库。如果您不想在当前目录中创建数据库，那么您可以指定带有路径的文件名，这样您就能在任意地方创建数据库。

`connection.cursor([cursorClass])` 该例程创建一个 cursor，将在 Python 数据库编程中用到。该方法接受一个单一的可选的参数 `cursorClass`。如果提供了该参数，则它必须是一个扩展自 `sqlite3.Cursor` 的自定义的 `cursor 类`。

`cursor.execute(sql [, optional parameters])` 该例程执行一个 SQL 语句。该 SQL 语句可以被参数化（即使用占位符代替 SQL 文本）。sqlite3 模块支持两种类型的占位符：问好和命名占位符（命名样式）。 例如：`cursor.execute("insert into people values (?, ?)", (who, age))`

`connection.execute(sql [, optional parameters])` 该例程是上面执行的由光标（cursor）对象提供的方法的快捷方式，它通过调用光标（cursor）方法创建了一个中间的光标对象，然后通过给定的参数调用光标的 `execute` 方法。

`connection.total_changes()` 该例程返回自数据库连接打开以来被修改、插入或删除的数据库总行数。

`cursor.fetchone()` 该方法获取查询结果集中的下一行，返回一个单一的序列，当没有更多可用的数据时，则返回 `None`。

`cursor.fetchmany([size=cursor.arraysize])` 该方法获取查询结果集中的下一行组，返回一个列表。当没有更多的可用的行时，则返回一个空的列表。该方法尝试获取由 `size` 参数指定的尽可能多的行。

`cursor.fetchall()` 该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。

## with con:

```python
import sqlite3 as lite
con = lite.connect('test.db')

with con:
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data
```

## executemany()

`cursor.executemany(sql, seq_of_parameters)` 该例程对 seq_of_parameters 中的所有参数或映射执行一个 SQL 命令。`connection.executemany(sql[, parameters])` 该例程是一个由调用光标（cursor）方法创建的中间的光标对象的快捷方式，然后通过给定的参数调用光标的 `executemany 方法`。

```python
cur = con.cursor()
cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
```

```python
cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
)
cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
```

### executescript()

`cursor.executescript(sql_script)` 该例程一旦接收到脚本，会执行多个 SQL 语句。它首先执行 COMMIT 语句，然后执行作为参数传入的 SQL 脚本。所有的 SQL 语句应该用分号（;）分隔。`connection.executescript(sql_script)` 该例程是一个由调用光标（cursor）方法创建的中间的光标对象的快捷方式，然后通过给定的参数调用光标的 `executescript 方法`。

```python
cur.executescript('''
  DROP TABLE IF EXISTS Cars;
  CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
  INSERT INTO Cars VALUES(1,'Audi',52642);
  INSERT INTO Cars VALUES(2,'Mercedes',57127);
  ''')
```

## con.rollback()

`connection.rollback()` 该方法回滚自上一次调用 `commit()` 以来对数据库所做的更改。

```python
try:
except lite.Error, e:

    if con:
        con.rollback()

    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if con:
        con.close()
```

### cur.lastrowid

`lid = cur.lastrowid`

### Row(dictionary cursor)

```python
with con:
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Cars")
    rows = cur.fetchall()
    for row in rows:
        print "%s %s %s" % (row["Id"], row["Name"], row["Price"])
```

### Parameterized queries

```python
cur.execute("UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))
```

The second example uses parameterized statements with named placeholders.

```python
cur.execute("SELECT Name, Price FROM Cars WHERE Id=:Id", {"Id": uId})
```

### Inserting images

For this example, we create a new table called Images. For the images, we use the BLOB data type, which stands for Binary Large Objects.

```python
fin = open("woman.jpg", "rb")
img = fin.read()
binary = lite.Binary(img)
cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,) )
```

### Reading images

```python
fout = open('woman2.jpg','wb')
fout.write(data)
cur.execute("SELECT Data FROM Images LIMIT 1")
data = cur.fetchone()[0]
```

### Metadata

Metadata in SQLite can be obtained using the `PRAGMA` command. SQLite objects may have attributes, which are metadata. Finally, we can also obtain specific metatada from querying the SQLite system `sqlite_master` table.

#### PRAGMA table_info(Cars)

```python
cur.execute('PRAGMA table_info(Cars)')
data = cur.fetchall()
for d in data:
    print d[0], d[1], d[2]
```

The `PRAGMA table_info(tableName)` command returns one row for each column in the Cars table. Columns in the result set include the **column order number**, **column name**, **data type**, **whether or not the column can be NULL**, and the **default value** for the column.

```python
0 Id INT
1 Name TEXT
2 Price INT
```

#### cur.description

```python
cur.execute('SELECT * FROM Cars')
col_names = [cn[0] for cn in cur.description]
rows = cur.fetchall()
print "%s %-10s %s" % (col_names[0], col_names[1], col_names[2])
for row in rows:
    print "%2s %-10s %s" % row
```

#### sqlite_master

```python
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    for row in rows:
        print row[0]
```

```python
Images
sqlite_sequence
Salaries
Cars
```

SQLite数据库中一个特殊的名叫 SQLITE_MASTER 上执行一个SELECT查询以获得所有表的索引。 每一个 SQLite 数据库都有一个叫 SQLITE_MASTER 的表，它定义数据库的模式。 `SQLITE_MASTER` 表看起来如下：

```SQL
CREATE TABLE sqlite_master (
type TEXT,
name TEXT,
tbl_name TEXT,
rootpage INTEGER,
sql TEXT
);
```

**对于表** 来说，type 字段永远是 ‘table’，name 字段永远是表的名字。所以，要获得数据库中所有表的列表， 使用下列SELECT语句：

```SQL
SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;
```

**对于索引**，`type` 等于 `‘index’`, `name` 则是索引的名字，`tbl_name` 是该索引所属的表的名字。 不管是表还是索引，sql 字段是原先用 `CREATE TABLE` 或 `CREATE INDEX` 语句创建它们时的命令文本。对于自动创建的索引（用来实现 `PRIMARY KEY` 或 `UNIQUE` 约束），sql字段为NULL。

`SQLITE_MASTER` 表是只读的。不能对它使用 `UPDATE`、`INSERT` 或 `DELETE`。 它会被 `CREATE TABLE`、`CREATE INDEX`、`DROP TABLE` 和 `DROP INDEX` 命令自动更新。

临时表不会出现在 `SQLITE_MASTER` 表中。临时表及其索引和触发器存放在另外一个叫 `SQLITE_TEMP_MASTER` 的表中。`SQLITE_TEMP_MASTER` 跟 `SQLITE_MASTER` 差不多， 但它只是对于创建那些临时表的应用可见。如果要获得所有表的列表， 不管是永久的还是临时的，可以使用类似下面的命令：

```SQL
SELECT name FROM
(SELECT * FROM sqlite_master UNION ALL
SELECT * FROM sqlite_temp_master)
WHERE type='table'
ORDER BY name
```

## Export Data

```python
def writeData(data):
    f = open('cars.sql', 'w')
    with f:
        f.write(data)
con = lite.connect(':memory:')
with con:
    cur = con.cursor()
    cur.execute(
    ...)
    data = '\n'.join(con.iterdump())
    writeData(data)
```

```python
data = '\n'.join(con.iterdump())
```

The `con.iterdump()` returns an iterator to dump the database in an SQL text format. The built-in `join()` function takes the iterator and joins all the strings in the iterator separated by a new line. This data is written to the `cars.sql` file in the `writeData()` function.

```SQL
BEGIN TRANSACTION;
CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
...
COMMIT;

```

## Import Data

```python
f = open('cars.sql', 'r')
    with f:
        data = f.read()
        return data
con = lite.connect(':memory:')
with con:
    cur = con.cursor()
    sql = readData()
    cur.executescript(sql)
```

## Transactions

In SQLite, any command other than the `SELECT` will start an implicit transaction.

SQLite supports three non-standard transaction levels: `DEFERRED`, `IMMEDIATE` and `EXCLUSIVE`. SQLite Python module also supports an autocommit mode, where all changes to the tables are immediately effective. we do not call the `commit()` command explicitly. But this time, the data is written to the Friends table.

```python
cur.execute("CREATE TABLE IF NOT EXISTS Temporary(Id INT)")
```

This SQL statement will create a new table. It also commits the previous changes.

In the autocommit mode, an SQL statement is executed immediately.

```python
con = lite.connect('test.db', isolation_level=None)
```

## SQLite类型

大多数的数据库引擎（到现在据我们所知的除了SQLite的每个sql数据库引擎）都使用静态的、刚性的类型，使用静态类型，数据的类型就由它的容器决定，这个容器是这个指被存放的特定列。 SQLite使用一个更一般的动态类型系统，sqlite中，值的数据类型跟值本身相关，而不是与它的容器相关。Sqlite的动态类型系统和其他数据库的更为一般的静态类型系统相兼容，但同时，sqlite中的动态类型允许它能做到一些传统刚性类型数据库所不可能做到的事。

### 存储类和数据类型

每个存放在sqlite数据库中（或者由这个数据库引擎操作）的值**都有下面中的一个存储类**：

-   NULL，值是NULL
-   INTEGER，值是有符号整形，根据值的大小以1,2,3,4,6或8字节存放
-   REAL，值是浮点型值，以8字节IEEE浮点数存放
-   TEXT，值是文本字符串，使用数据库编码（UTF-8，UTF-16BE或者UTF-16LE）存放
-   BLOB，只是一个数据块，完全按照输入存放（即没有准换）

从上可以看出存储类比数据类型更一般化。比如INTEGER存储类，包括6中不同长度的不同整形数据类型，这在磁盘上造成了差异。但是只要INTEGER值被从磁盘读出进入到内存进行处理，它们被转换成最一般的数据类型（8-字节有符号整形）。 Sqlite v3数据库中的任何列，除了整形主键列，可以用于存储任何一个存储列的值。sql语句中的中所有值，不管它们是嵌入在sql文本中或者是作为参数绑定到一个预编译的sql语句，它们的存储类型都是未定的。在下面描述的情况中，数据库引擎会在查询执行过程中在数值（numeric）存储类型（INTEGER和REAL）和TEXT之间转换值。

#### 布尔类型

Sqlite没有单独的布尔存储类型，它使用INTEGER作为存储类型，0为false，1为true

#### Date和Time Datatype

Sqlite没有另外为存储日期和时间设定一个存储类集，内置的sqlite日期和时间函数能够将日期和时间以TEXT，REAL或INTEGER形式存放

-   TEXT 作为IS08601字符串（"YYYY-MM-DD HH:MM:SS.SSS"）
-   REAL 从格林威治时间11月24日，4174 B.C中午以来的天数
-   INTEGER 从 1970-01-01 00:00:00 UTC以来的秒数

程序可以任意选择这几个存储类型去存储日期和时间，并且能够使用内置的日期和时间函数在这些格式间自由转换

### 类型近似(SQLite Type Affinity)

近似的规则:

| 类型             | INTEGER  |
|------------------|----------|
| INT              | INT8     |
| TINYINT          | SMALLINT |
| MEDIUMINT        | BIGINT   |
| UNSIGNED BIG INT | INT2     |

| 类型                   | TEXT          |
|------------------------|---------------|
| CHARACTER(20)          | VARCHAR(255)  |
| VARYING CHARACTER(255) | NCHAR(55)     |
| NATIVE CHARACTER(70)   | NVARCHAR(100) |
| TEXT                   | CLOB          |

| 类型 | NONE                  |
|------|-----------------------|
| BLOB | no datatype specified |

| 类型             | REAL   |
|------------------|--------|
| REAL             | DOUBLE |
| DOUBLE PRECISION | FLOAT  |

| 类型     | NUMERIC       |
|----------|---------------|
| DATETIME | DECIMAL(10,5) |
| BOOLEAN  | DATE          |

NCHAR、NVARCHAR、NTEXT。这三种从名字上看比前面三种多了个“N”。它表示存储的是Unicode数据类型的字符。

In SQLite, `INTEGER PRIMARY KEY` column is auto incremented. There is also an `AUTOINCREMENT` keyword. When used in `INTEGER PRIMARY KEY AUTOINCREMENT` a slightly different algorithm for Id creation is used.

使用SQLAlchemy
--------------
未完..

### 参考文献
[SQLite Python tutorial](http://zetcode.com/db/sqlitepythontutorial/)
[使用SQLite](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001388320596292f925f46d56ef4c80a1c9d8e47e2d5711000)
