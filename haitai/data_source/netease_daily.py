import time
import haitai
import os
"""

"""
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
        return None

    cmd=('wget "'+url+'''" -q -O - | iconv -f gbk >  %(f)s''')%{
            'a': stock_id,'f': stock_file,
            'today': today}
    time.sleep(1) # sleep for not being blocked
    os.system(cmd)

    return get_today(stock_file)
    
