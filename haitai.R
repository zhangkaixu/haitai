# 
#
#
#
#

library(quantmod)

grep.name <- function(x) csrcindustry[grepl(x,csrcindustry[,2]),c(1,2)]
grep.ind <- function(x) csrcindustry[grepl(x,csrcindustry[,4]),c(1,2,4)]

# 为yahoo的query加上后缀（支持向量）
add.yahoo.postfix=function(x) paste(x,c(c('.sz','.ss')[grepl('^[69]',x)+1],'')[grepl('s[sz]',x)+1],sep='')

log.data=function(x){
    eval.parent(substitute(x[,1]<-log(x[,1])))
    eval.parent(substitute(x[,2]<-log(x[,2])))
    eval.parent(substitute(x[,3]<-log(x[,3])))
    eval.parent(substitute(x[,4]<-log(x[,4])))
    eval.parent(substitute(x[,5]<-log(x[,5]+1)))
}


top.symbols = function() csrcindustry[grep("^(0|6)00(1|0)",csrcindustry[,1]),2]
#top.symbols = function() csrcindustry[grep("^(0|6)000(1|0)",csrcindustry[,1]),2]

as.yahoo.symbol = function(what) {
    if (grepl('^[^0-9]+',what)){
        what=add.yahoo.postfix(csrcindustry[csrcindustry[,2]==what,1])
    }else{
        what=add.yahoo.postfix(what)
    }
    return(what)
}

download.yahoo.csv = function(symbol){
    symbol=as.yahoo.symbol(symbol)
    system(paste('haitai/scripts/yahoo.py today',symbol))
}

read.yahoo.csv = function(symbol) {
    symbol=as.yahoo.symbol(symbol)
    symbol_path=paste('data/yahoo_daily/',symbol,sep='')
    if(!file.exists(symbol_path)){
        download.yahoo.csv(symbol)
    }
    if (file.info(symbol_path)$size==0) return(NULL)
    #print(file.info(symbol_path)$size)
    symbol=read.csv(symbol_path)
    tmp.symbol=symbol[symbol[,6]!=0,]
    if (nrow(tmp.symbol)!=0) symbol=tmp.symbol
    symbol=xts(symbol[,2:6],as.POSIXct(symbol[,1]))
    return(symbol)
}
gupiao=read.yahoo.csv
kxian=function(x,time.index='') candleChart(gupiao(x)[time.index])

mean.price=function(symbols){
    m=read.yahoo.csv('000001.ss')
    m[,4]=0
    for ( s in symbols ) {
        print(s)
        d=read.yahoo.csv(s)
        if(is.null(d))next
        d=log(d[,4])
        m[index(d),5]=m[index(d),5]+1
        d=d-as.numeric(last(d)[1,1])
        m[index(d),4]=m[index(d),4]+d
    }
    m[,4]=m[,4]/m[,5]
    return(m)
}


pair.chart=function(a,b,use.log=FALSE,use.close=FALSE){
    if(use.close){
        a=a[,4]
        b=b[,4]
    }
    if(use.log) {
        a=log(a)
        b=log(b)
    }
    par(mfrow=c(2,1))
    plot(a-b)
    plot(a-as.numeric(last(a)[1,1]),main='')
    lines(b-as.numeric(last(b)[1,1]),col='blue')
    par(mfrow=c(1,1))
}


### initialization

# load csrc industry table
csrcindustry=read.csv("meta/csrcindustry.csv",colClasses=c('NULL','character','character','NULL','NULL','NULL','factor','NULL','NULL','character','NULL'))
csrcindustry[,2]=gsub(' ','',csrcindustry[,2])  # 去掉多余空格
csrcindustry[,2]=gsub('Ａ','A',csrcindustry[,2])  #
colnames(csrcindustry)[1]<-'code'
colnames(csrcindustry)[2]<-'name'
colnames(csrcindustry)[3]<-'c.ind'
colnames(csrcindustry)[4]<-'full.ind'

all.symbols <- getOption("getSymbols.sources")
for ( i in 1:nrow(csrcindustry) ){
    all.symbols[[as.character(csrcindustry[i,2])]] <- list(name=add.yahoo.postfix(csrcindustry[i,1]),
                                                           src='yahoo')
}
options(getSymbols.sources = all.symbols)
