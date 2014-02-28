haitai
======

haitai

依赖
---------------------
python3
cherrypy
python3-mako


R 语言部分
---------------------------------
使用了 `quantmod` 包

使用 `library(haitai)` 导入

    kxian('同方股份','2013/') # 直接查看同方股份的k线图
    tfgf=gupiao('同方股份') # 得到同方股份日交易历史记录
