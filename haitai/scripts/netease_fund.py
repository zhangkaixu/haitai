#coding:utf8
from __future__ import print_function
import datetime
import requests
import sys

def get_163(url):
    """
    获得一页的价格信息
    """
    res = requests.get(url)
    cont = res.content
    cont= cont.split(b'fn_cm_table')[-1]
    cont = cont.split(b'mod_pages')[0]

    ln = 0
    dates = []
    values = []
    ac_values = []
    for l in cont.splitlines():

        l = l.strip()
        if l.startswith(b'<td>'):
            ln = ln + 1
            if ln % 4 == 1 :
                #dates.append(l[4:-5])
                dates.append(l[4:-5].decode('gbk'))
            if ln % 4 == 2 : 
                values.append(float(l[4:-5]))
            if ln % 4 == 3 :
                ac_values.append(float(l[4:-5]))
    return (
        list(dates), 
        list(values),
        list(ac_values),
        )
def print_fund(code):
    url = '''http://quotes.money.163.com/fund/jzzs_%(code)s_%(page)d.html?start=1015-06-01&end=3017-04-14&order=asc'''

    #code = '159919'
    page = 0
    recs = None
    names = u'日期,单位净值,累计净值'.split(',')
    while True :
        #print(page)

        req = url%{'code':code, 'page':page}
        data = get_163(req)


        if not data[0] : break

        if recs is None :
            recs = list(data)
        else :
            for i in range(len(data)):
                #print(i)
                #print(recs[i])
                #print(data[i])
                recs[i] += data[i]
        page += 1
        #break

    print(','.join(names).encode('utf8'))
    for i in range(len(recs[0])):
        print(*[(recs[j][i]) for j in range(len(recs))], sep = ',')

if __name__ == '__main__':
    if len(sys.argv) < 2 :
        exit()
        
    print_fund(sys.argv[1])
