#!/usr/bin/python3
import time
import sys
import os
import random

help_text="""使用163下载股票每日历史数据

./163.py date dest stock_id*
    date ： 2013-11-01 或 20131101
    dest ： data 或 . 神马的
    stock_id ： 000629.sz 
    
例如：
    ./haitai/scripts/163.py 2013-11-01 data `cat data/index_ids.txt`"""

url="""http://quotes.money.163.com/service/chddata.html?code=%(a)s&end=%(today)s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"""

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
    stock_ids=sys.argv[3:]
    today=sys.argv[1]
    today=today.replace('-','')
    dest=os.path.join(sys.argv[2],'163_daily')

    

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
        stock_file=os.path.join(dest,stock_file)

        last=get_today(stock_file)
        if last and ''.join(last.split('-'))==today : 
            #print("%s alread today"%(stock_id))
            continue


        cmd=('wget "'+url+'''" -q -O - | iconv -f gbk >  %(f)s''')%{
                'a':stock_id,'f': stock_file,
                'today': today}
        if i+1 !=len(stock_ids) :
            #time.sleep(1+random.random()*3)
            time.sleep(1)
        #print(cmd)
        os.system(cmd)

        last=get_today(stock_file)
        now=time.time()
        sec_left=(now-start_time)/(i+1)*(n-i-1)
        print(stock_id,last)
        print("%.2f%% %.2f"%((i+1)/n*100,sec_left),end='\r')

