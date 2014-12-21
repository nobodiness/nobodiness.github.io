Title: 我的第一个Github博客
Date: 2014-12-19 19:17
Category: Python
Tags: Pelican,静态博客
Author: 阿七
Summary: 搭建这个博客的方法

我一直相信如果可以一定要用最简单个技术来实现一切.  
所以呢,看到静态博客就觉得很喜欢,一定要整一个

静态博客的技术有很多,现在最火的是Jekyll,为什么要用Pelican?  
主要是还是因为喜欢Python.

不过说实在的Pelican的模板比Jekyll的少多了,质量也比较差.  
外貌党 + 不愿意(HUI)自己做网页的人(就像我T_T) 真心不推荐  

除了我现在用的这个(Octopress模板改过来的)  
还有几个我感觉也比较好:

[Elegant](http://oncrashreboot.com/elegant-best-pelican-theme-features)  
[Pure Pelican Theme](http://purepelican.com)  
[SVBTLE](https://github.com/wting/pelican-svbtle)  
[zurb-F5-basic](https://github.com/getpelican/pelican-themes/tree/master/zurb-F5-basic)  
[aboutwilson](https://github.com/getpelican/pelican-themes/tree/master/aboutwilson)  
[Chunk for Pelican](https://github.com/tbunnyman/pelican-chunk)  
[tuxlite_tbs](https://github.com/getpelican/pelican-themes/tree/master/tuxlite_tbs)  
[Gum](https://github.com/getpelican/pelican-themes/tree/master/gum)  
[PELICAN-CAIT](http://ptd.pronoiac.org/pelican-cait/)  

过一段时间,我打算从Jekyll改一部分模板过来  
Pelican模板引擎用的[Jinja2](http://jinja.pocoo.org)
Jekyll 模板引擎用的[Liquid](http://docs.shopify.com/themes/liquid-documentation/basics)

Pelican官方文档在[这里](http://docs.getpelican.com/en/3.5.0/index.html)

## 安装Pelican
```bash
$sudo pip install pelican markdown
```

## 开设一个目录
```bash
$mkdir /path/to/your/blog
$cd /path/to/your/blog
```
## 快捷安装
```bash
$pelican-quickstart
```

## 写一篇文章
在 content 目录新建一个 `test.md`文件, 填入一下内容:
```markdown
Title: 第一篇Github博客
Date: 2014-12-19 19:17
Category: Python
Tags: Pelican,静态博客
Author: 阿七
Summary: 搭建这个博客的方法

这里是内容
```
放到生成的`content`文件夹里
然后执行:
```bash
$make html
$make serve
```
开启一个测试服务器, 这会在本地`8000`端口建立一个测试web服务器, 
使用浏览器打开: `http://localhost:8000` 来访问这个测试服务器, 然后就可以欣赏到你的博客了

## 修改配置
[这里](http://docs.getpelican.com/en/3.5.0/settings.html)是官方教程
可以参考中文翻译中的[这里](http://pelican-zh.readthedocs.org/en/latest/zh-cn/settings/)

在`pelicanconf.py`中修改如下
```python
AUTHOR = u'默认作者'
SITENAME = u'博客的名字'
# 修改时区
TIMEZONE = 'Asia/Shanghai'
# 修改语言
DEFAULT_LANG = u'cn'
# 修改时间格式
DEFAULT_DATE_FORMAT = '%Y %B %d %a'
```

## 安装模板
我用的是`Octopress Theme for Pelican`

在[这里](https://github.com/duilio/pelican-octopress-theme)

复制一份到本地:
```bash
$git clone git://github.com/duilio/pelican-octopress-theme.git
```

在`pelicanconf.py`中修改如下

```python
THEME = "pelican-octopress-theme"
```

也可以加入自己的Github账号:

```python
GITHUB_USER = "nobodiness"
GITHUB_REPO_COUNT = 5
GITHUB_SKIP_FORK = False
GITHUB_SHOW_USER_LINK = False
```

## 评论系统
Disqus的评论怎么也弄不好,真邪门
然后就用的多说的,也不错
再说一句,Disqus对中文的支持也不好
文章题目是中文也不行 :-(
在`article.html`中加入以下代码
```html
<!-- 多说评论框 start -->
<div class="ds-thread" data-thread-key="{{ article.url }}" 
data-title="{{ article.title }}" data-url="{{ SITEURL }}/{{ article.url }}"></div>
<!-- 多说评论框 end -->
<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
<script type="text/javascript">
var duoshuoQuery = {short_name:"nobodiness"};
(function() {
var ds = document.createElement('script');
ds.type = 'text/javascript';ds.async = true;
ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:')
 + '//static.duoshuo.com/embed.js';
ds.charset = 'UTF-8';
(document.getElementsByTagName('head')[0]
|| document.getElementsByTagName('body')[0]).appendChild(ds);
})();
</script> 
<!-- 多说公共JS代码 end --> 
``` 

## Markdown扩展
可以给原生markdown加入扩展.可以看[这里](http://pythonhosted.org/Markdown/extensions/extra.html)
```python
MD_EXTENSIONS = ['codehilite','extra','nl2br']
```
`codehilite`:代码高亮
`nl2br`:真换行

## 代码高亮
~~原生的Octopress模板没有带代码高亮的css~~
(其实是有的,上面加扩展的时候,像下面这样写就好了)
```python
MD_EXTENSIONS = ['codehilite(css=highlight)','extra','nl2br']
```

我们给他加上

代码高亮的CSS[这里](http://richleland.github.io/pygments-css/)有很多
我这里选择monokai这个
下载CSS文件加入`static/css/`文件中
在模板中的base.html文件`<head>`标签中加入
```html
<link href="{{ SITEURL }}/theme/css/monokai.css" media="screen, projection" 
rel="stylesheet" type="text/css">
```


关于Pelican后面会有更详细的分析

#### 以下是我参考的几篇教程:

[使用Pelican打造静态博客](http://www.linuxzen.com/shi-yong-pelicanda-zao-jing-tai-bo-ke.html)
[用 Pelican 和 GitHub Pages 搭建免费的个人博客](http://www.dongxf.com/3_Build_Personal_Blog_With_Pelican_And_GitHub_Pages.html)
[一步一步打造Geek风格的技术博客](http://blog.csdn.net/poem_of_sunshine/article/details/12913325)

