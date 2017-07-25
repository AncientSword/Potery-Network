# -*- coding: utf-8 -*-
import sys
from langconv import Converter
#将简体转换成繁体
def simpleToTradition(line):    
    line = Converter('zh-hant').convert(line.decode('gbk','ignore'))
    return line  
#设置编码
reload(sys)
sys.setdefaultencoding('gbk')
#打开读写文件
fread=open('D:\study information\Interesting Programmes\python\potery network\data\qts_simple.txt','r')
fwrite=open('D:\study information\Interesting Programmes\python\potery network\data\qtsupdate.txt','w')
for eachline in fread:  #对每行进行简繁转换
    content=eachline.lstrip()   #去除该行左边空格
    if(content):
        fwrite.write(simpleToTradition(content))
fread.close()
fwrite.close()
print 'over'
