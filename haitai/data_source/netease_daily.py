import time
import haitai
import haitai.common
import os
import numpy as np
"""

"""

def load_fresh_stock(stock_id,dates,vind=10, nov = False) :
    stock_file=os.path.join('./data/163_daily/',stock_id)

    if not os.path.exists(stock_file) :
        return None

    raw=list(open(stock_file))[1:]
    if not raw : return None

    today,cd,name,*_=raw[0].split(',')
    if today!= dates[0] : 
        print('not today',name,cd,dates[0])
        return None

    price=haitai.common.gen_price(raw,len(dates), vind = vind, nov = nov)
    min_days=len(price)
    volum=np.array([x[2] for x in price])
    price=np.array([x[1] for x in price])
    price/=price[0]
    return name,price,volum


def get_today(stock_file):
    if os.path.exists(stock_file) :
        for k,l in enumerate(open(stock_file)):
            if k == 1 :
                l=l.split(',')[0]
                return l
    return None

def refresh_stock(stock_id,today):
    """
    如果最新日期不是today,则更新 stock_id 这只股票的记录
    """
    url="""http://quotes.money.163.com/service/chddata.html?code=%(a)s&end=%(today)s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"""
    dest=haitai.daily_dir
    if '.' in stock_id :
        stock_id,_,mkt=stock_id.partition('.')
        if mkt=='sz' :
            stock_id='1'+stock_id
        else :
            stock_id='0'+stock_id
    if len(stock_id) == 6:
        if stock_id[0] == '6' :
            stock_id='0'+stock_id
        else :
            stock_id='1'+stock_id


    stock_file=stock_id[1:]+'.'+('ss' if stock_id[0]=='0' else 'sz')
    stock_file=os.path.join(dest,stock_file)

    last=get_today(stock_file)
    if last and ''.join(last.split('-'))==today : 
        #print("%s alread today"%(stock_id))
        return None

    cmd=('wget "'+url+'''" -q -O - | iconv -f gbk >  %(f)s''')%{
            'a': stock_id,'f': stock_file,
            'today': today}
    time.sleep(1) # sleep for not being blocked
    os.system(cmd)

    return get_today(stock_file)
    
