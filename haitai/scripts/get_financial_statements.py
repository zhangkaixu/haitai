#!/usr/bin/python3

import haitai
import os
import time

if __name__ == '__main__':
    print('get financial statements')
    cmdtmp="""wget "http://quotes.money.163.com/service/cwbbzy_%(code)s.html" -q -O - | iconv -f gbk  > %(path)s/%(code)s.fs"""
    path=os.path.join(haitai.data_dir,'financial_statements')
    os.system('mkdir -p '+path)
    for line in open(haitai.stock_ids):
        line=line.strip()
        code=line[:6]
        cmd=cmdtmp%{'path':path,'code':code}
        os.system(cmd)
        print(code)
        time.sleep(2)
        


