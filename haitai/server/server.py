#!/usr/bin/python3
import cherrypy
from jinja2 import Template
import haitai
import os

"""
you may need a config file such as :
    
    [global]
    server.socket_host = "your IP"
    server.socket_port = 8080
"""

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

    exposed = True
    def GET(self,stock_id=None):
        if stock_id == None :
            index_html=open('./haitai/server/figs_template.html').read()
            template=Template(index_html)
            html = template.render({"menu" : self.show_list()})
            return html

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

    cherrypy.config.update("server.config")

    cherrypy.tree.mount(
                Figs(), '/figs',
                {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}},
            )
    cherrypy.engine.start()
    cherrypy.engine.block()
