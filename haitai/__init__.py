import os
import numpy as np
import datetime


#####    meta_dir
meta_dir='meta'

stock_ids=os.path.join(meta_dir,'stock_ids.txt') ## 股票代码列表
index_ids=os.path.join(meta_dir,'index_ids.txt') ## 指数代码列表
industries=os.path.join(meta_dir,'industries.txt')

####   数据总目录
data_dir='data'

# 每日历史记录目录
daily_dir=os.path.join(data_dir,'163_daily')

"""output"""

output_dir='output'


## 函数

def symbol_to_filename(symbol):
    # 简便的方法 for daily数据
    if symbol[0]=='0' :
        return os.path.join(daily_dir,symbol+'.sz')
    else :
        return os.path.join(daily_dir,symbol+'.ss')


def from_symbols_list_file(filename):
    return [line.strip() for line in open(filename)]

def load_recent_dates(ndays=100,index='399001.sz'):
    index300=os.path.join(daily_dir,index)
    x=os.popen('head -n %d %s'%(ndays+1,index300)).read().splitlines()[1:]
    x=[l.split(',') for l in x]
    days=[l[0] for l in x]
    return days

def get_symbol_list(bk='主板'):
    li = open(stock_ids).read().splitlines()[1:]
    if bk =='主板' :
        return [x for x in li if x[:3]!='002']
    return []
    
    #return [line.strip() for line in open(haitai.stock_ids)]

def load_industries():
    d=dict()
    for line in open(industries) :
        line=line.strip()
        s,_,others=line.partition(' ')
        s+='.sz' if s[0]=='0' else '.ss'
        others,_,ind=others.rpartition(' ')
        others,_,big=others.rpartition(' ')
        ind=big+'-'+ind
        if ind not in d : d[ind]=[]
        d[ind].append(s)
    return d

def load_names():
    d=dict()
    for line in open(industries) :
        line=line.strip()
        s,_,others=line.partition(' ')
        s+='.sz' if s[0]=='0' else '.ss'
        others,_,ind=others.rpartition(' ')
        others,_,big=others.rpartition(' ')
        d[s]=(others)
    return d


def gen_array(symbol,ndays=100):
    filename=os.path.join(daily_dir,symbol)
    x=os.popen('head -n %d %s'%(ndays+1,filename)).read().splitlines()[1:]
    x=[l.split(',') for l in x]
    name=x[0][2]
    days=[[l[0],l[3],float(l[7])] for l in x]
    
    k=1
    last=None
    for i,day in enumerate(days) :
        flag=False
        if day[1]=='' or day[1]=='0.0': 
            flag=True
            day[1]=day[2]
        else : 
            day[1]=float(day[1])
        if last==None :
            last=day[2]
        else :
            if last!=day[1] :
                k=k*day[1]/last
                pass
            last=day[2]
        day[1]/=k
        #if flag  : return None,None,None
    dates,prices,_=(zip(*days))
    return name,dates,prices

def daily(symbol,ndays=100):
    filename=os.path.join(daily_dir,symbol)
    x=os.popen('head -n %d %s'%(ndays+1,filename)).read().splitlines()[1:]
    x=[l.split(',') for l in x]
    name=x[0][2]
    days=[[l[0],l[3],float(l[7])] for l in x]
    
    k=1
    last=None
    for i,day in enumerate(days) :
        flag=False
        if day[1]=='' or day[1]=='0.0': 
            flag=True
            day[1]=day[2]
        else : 
            day[1]=float(day[1])
        if last==None :
            last=day[2]
        else :
            if last!=day[1] :
                k=k*day[1]/last
                pass
            last=day[2]
        day[1]/=k
        #if flag  : return None,None,None
    dates,prices,_=(zip(*days))
    prices=np.array(prices)
    dates=[list(map(int,date.split('-')))for date in dates]
    dates=[datetime.date(*date) for date in dates]
    return {'name':name,'date':dates,'price':prices,'symbol':symbol}


def symbols(syms=set()):
    for line in open(stock_ids) :
        line=line.strip()
