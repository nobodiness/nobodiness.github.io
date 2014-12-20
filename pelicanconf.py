#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'阿七'
SITENAME = u'一个博客'
SITEURL = 'nobodiness.github.io'
RELATIVE_URLS = True
# PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MD_EXTENSIONS = ['codehilite(css_class=codehilite)','extra','nl2br']

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('我的豆瓣', 'http://www.douban.com/people/53955651/'),)
          # ('我的微博', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
# OUTPUT_PATH ('nobodiness.github.io/')
DEFAULT_DATE_FORMAT = '%Y %B %d %a'
# DISQUS_SITENAME = u"nobodiness"

THEME = "pelican-octopress-theme"

# DISPLAY_CATEGORIES_ON_MENU = False

GITHUB_USER = "nobodiness"
GITHUB_REPO_COUNT = 5
GITHUB_SKIP_FORK = False
GITHUB_SHOW_USER_LINK = False

# QR_CODE = True

# SIDEBAR_IMAGE: # Adds specified image to sidebar. Example value: "images/author_photo.jpg"
# SEARCH_BOX = True #set to true to enable site search box
