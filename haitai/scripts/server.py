#!/usr/bin/python3

import cherrypy
import haitai
import os

def get_svg(path):
    if path == 'whole' or path == 'mean' :
        return open('./output/主板_%s.svg'%path,'r').read()

    if path[0]=='0' :
        path=path+'.sz'
    else :
        path = path + '.ss'
    d="./output/figs/"+path + '.svg'
    if not os.path.exists(d) : return None
    return open(d,'r').read()


class Figs(object):
    def show_list(self):
        inds=haitai.load_industries()
        names=haitai.load_names()
        x=[]
        for k,v in inds.items():
            y=[k]
            for i in v :
                code,ins=i.split('.')
                if code.startswith('002'): continue
                y.append("<a onclick='open_stock(\"%s\")'>%s,%s</a>"%(code,names[i],i))
            x.append("<br/>".join(y))
        return "<br/>".join(x)

    index_html=""" <!DOCTYPE html>
<html>
<head>
<style type="text/css">
div#container{width:100%%}
div#header {background-color:#99bbbb;}
div#menu {background-color:#ffff99;  height:80%%;position:absolute;  width:20%%; float:left;overflow:auto;}
div#content {background-color:#EEEEEE;width:80%%; height:80%%; float:right;overflow:auto;}
div#footer {background-color:#99bbbb; clear:both; text-align:center;}
h1 {margin-bottom:0;}
h2 {margin-bottom:0; font-size:14px;}
ul {margin:0;}
li {list-style:none;}
</style>
</head>

<body>

<div id="container">

<div id="header">
<h1>Main Title of Web Page</h1>
</div>

<div id="menu">
%(menu)s
</div>

<div id="content">
<iframe id="if" width=100%% height=100%% ></iframe>
</div>

<div id="footer">Copyright W3School.com.cn</div>

</div>

</body>
<script>
function open_stock(stock_id){
        document.getElementById("if").src="http://aliyun:8080/figs/"+stock_id
}
open_stock("mean")
</script>
</html>"""
    exposed = True
    def GET(self,stock_id=None):
        if stock_id == None :
            return self.index_html%{"menu":self.show_list()}
        svg=get_svg(stock_id)
        if svg is None : return "no such stock"

        return "<svg>%s</svg>"%(svg)
        return "stock id is %s"%(stock_id)


if __name__ == '__main__':
    l=haitai.get_symbol_list()
    l=sorted(l)
    l=[x.split('.')[0] for x in l]
    stock_list=l
    stock_order={k:v for v,k in enumerate(stock_list)}




    cherrypy.config.update({'server.socket_host': '115.28.22.82',
                                'server.socket_port': 8080, })
    #cherrypy.quickstart(HelloWorld())

    cherrypy.tree.mount(
                Figs(), '/figs',
                {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
            )
    cherrypy.engine.start()
    cherrypy.engine.block()
