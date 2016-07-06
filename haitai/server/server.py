#!/usr/bin/python3
import cherrypy
from jinja2 import Template
import haitai
import os

import haitai.diff

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
        for k,v in sorted(inds.items()):
            y=['<b>%s</b>'%(k)]
            for i in v :
                code,ins=i.split('.')
                if code.startswith('002'): continue
                y.append("<a onclick='open_stock(\"%s\")'>%s,%s</a>"%(code,names[i],i))
            x.append("<br/>".join(y))
        return "<br/>".join(x)

    exposed = True
    def GET(self,stock_id=None):
        if stock_id == None : # the default page
            index_html=open('./haitai/server/figs_template.html').read()
            template=Template(index_html)
            html = template.render({"menu" : self.show_list()})
            return html

        if stock_id == 'whole' or stock_id == 'mean' :
            svg = open('./output/主板_%s.svg'%stock_id,'r').read()
            return "<svg>%s</svg>"%(svg)

        # one diff svg
        #svg=get_svg(stock_id)
        if '-' in stock_id :
            stock_a,_,stock_b = stock_id.partition('-')
        else :
            stock_a = stock_id
            stock_b = None
        svg = haitai.diff.diff_svg(stock_a, stock_b)
        if svg is None : return "no such stock"

        return "<svg>%s</svg>"%(svg)


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
