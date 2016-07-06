import pylab
def gen_ticks(dates):
    last_month=None
    last_year=None
    year_ticks=[[],[]]
    month_ticks=[[],[]]
    for ind,date in zip(range(0,-len(dates),-1),dates):
        date=date.split('-')
        month=date[0][3:]+date[1]
        year=date[0]
        #year+='-12' if int(date[1])>=7 else '-6'
        if year != last_year :
            last_year=year
            year_ticks[0].append(ind)
            year_ticks[1].append(year)

        if month !=last_month :
            last_month=month
            month_ticks[0].append(ind)
            month_ticks[1].append(date[1])
    return month_ticks,year_ticks

def draw_grid(ax,both_ticks):
    month_ticks,year_ticks=both_ticks
    pylab.grid()
    ax.xaxis.set_ticks(month_ticks[0],minor=True)
    pylab.xticks(year_ticks[0],year_ticks[1])
    pylab.grid(which='minor',color='pink')
    pylab.grid(which='major',color='black')

def draw_lines(ax,lines,log=False):

    max_y,min_y=None,None
    for args in lines :
        xs=list(range(0,-len(args[0]),-1))
        pylab.plot(xs,*args,linewidth=.5)
        pylab.xlim([min(xs),max(xs)+5])
        maxy=max(args[0])
        miny=min(args[0])
        if max_y==None or max_y<maxy : max_y=maxy
        if min_y==None or min_y>miny : min_y=miny
    pylab.ylim([min_y,max_y])
    if log :
        #ax.set_yscale('log')
        pass
