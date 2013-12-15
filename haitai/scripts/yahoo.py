#!/usr/bin/python3
import time
import sys
import os
import random
import datetime

import haitai

help_text="""使用yahoo下载股票每日历史数据

./163.py date [stocks]
    date ： 2013-11-01 或 20131101 或 today
    
例如：
    ./haitai/scripts/163.py 2013-11-01 # 下载所有指数信息
    ./haitai/scripts/163.py 2013-11-01 stocks # 下载所有股票信息"""

url="""http://quotes.money.163.com/service/chddata.html?code=%(a)s&end=%(today)s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"""

url="""http://chart.yahoo.com/table.csv?s=%(a)s&a=%(from_xm)s&b=%(from_d)s&c=%(from_y)s&d=%(to_xm)s&e=%(to_d)s&f=%(to_y)s&g=d&q=q&y=0&x=.csv"""

def get_today(stock_file):
    if os.path.exists(stock_file) :
        for k,l in enumerate(open(stock_file)):
            if k == 1 :
                l=l.split(',')[0]
                return l
    return None


if __name__ == '__main__':
    if len(sys.argv)==1 :
        print(help_text)
        exit()

    if len(sys.argv)>2 :
        stock_ids=[x.strip() for x in open(haitai.stock_ids)]
        if (sys.argv[2]=='stocks') :
            pass
        elif (sys.argv[2]=='top') :
            stock_ids=[i for i in stock_ids if i[1]=='0' and i[2]=='0' 
                    and (i[3]in '01')]
        else :
            stock_ids=sys.argv[2:]


    else :
        stock_ids=[x.strip() for x in open(haitai.index_ids)]


    today=sys.argv[1]
    if today=='today' :
        t=datetime.date.today()
        m=t.month
        if m<10 : m='0'+str(m)
        d=t.day
        if d<10 : d='0'+str(d)
        today=''.join(map(str,(t.year,m,d)))
    else :
        today=today.replace('-','')

    dest='data/yahoo_daily'

    

    print("下载截止日期为 %s 的 %s 只股票每日行情到目标 %s" %(today,len(stock_ids),dest))
    stock_ids=sorted(stock_ids)

    n=len(stock_ids)
    start_time=time.time()

    os.system('mkdir -p '+os.path.join(dest))

    for i,stock_id in enumerate(stock_ids) :

        stock_id,_,mkt=stock_id.partition('.')
        if mkt=='sz' :
            stock_id='1'+stock_id
        else :
            stock_id='0'+stock_id

        stock_file=stock_id[1:]+'.'+('ss' if stock_id[0]=='0' else 'sz')
        stock_id=stock_file

        stock_file=os.path.join(dest,stock_file)

        last=get_today(stock_file)
        if last and ''.join(last.split('-'))==today : 
            continue


        cmd=('wget "'+url+'''" -q -O %(f)s''')%{
                'from_xm':0, 'from_d':1, 'from_y':2007,
                'to_xm':11, 'to_d':15, 'to_y':2013,
                'a': stock_id,'f': stock_file,
                'today': today}

        if i+1 !=len(stock_ids) :
            time.sleep(1)
        os.system(cmd)

        last=get_today(stock_file)
        now=time.time()
        sec_left=(now-start_time)/(i+1)*(n-i-1)
        print(stock_id,last)
        print("%.2f%% %.2f"%((i+1)/n*100,sec_left),end='\r')

