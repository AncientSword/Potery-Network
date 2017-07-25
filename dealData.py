# -*- coding: utf-8 -*-
import sqlite3,csv
from Poem import Poem
from collections import Counter,defaultdict
#判断该行内容是否为标题及作者
def isTitle(line):
    finding1='「'
    finding2='」'    #利用「」寻找标题
    string=line.decode('gbk','ignore')    #转码
    finding1=finding1.decode('utf-8','ignore')
    finding2=finding2.decode('utf-8','ignore')
    begin=string.find(finding1)+1    #标题起始位置
    if(begin!=0):
        end=string.find(finding2)    #标题终止位置
        length=len(string)    #字符串长度
        if(length>end+1):       #若length>end 该行无作者名 该诗不予考虑
            title=string[begin:end]    #获取标题
            author=string[end+1:len(string)]    #获取作者名
            return (True,author,title)    #若为标题，返回判断、作者、标题
        else:
            return (False,'','')    #若不为标题，返回判断、空字符串      
    else:
        return (False,'','')    #若不为标题，返回判断、空字符串
#读取全唐诗，将诗歌存于列表，作者存于集合及列表
def read_qts(read_file_path):
    count = 0   #计数变量
    PoemList=[] #诗歌列表
    qtsauthor_set=set() #全唐诗作者集合
    qtsauthor_list=[]   #全唐诗作者列表
    text=[] #诗歌内容列表
    fread=open(read_file_path,'r')
    for eachline in fread:
        content=eachline.strip()    #清除该行空格
        judge,author,title=isTitle(content) #判断是否为标题
        if(judge):  #如果是标题，则更新前一首诗内容，添加新一首诗信息
            if(len(text)>0):
                PoemList[count-1].updateContent(text)
            text=[]
            PoemList.append(Poem(author,title,text))   
            qtsauthor_set.add(author)
            qtsauthor_list.append(author)
            count+=1
        else:
            if(content.startswith('1')==False):
                text.append(content)
    PoemList[count-1].updateContent(text)
    fread.close()
    return (PoemList,qtsauthor_set,qtsauthor_list)  #返回诗歌列表，全唐诗作者集合，全唐诗作者列表
#处理诗人信息列表
def dealPersonInfo(data_path):
    conn = sqlite3.connect(data_path)   #连接数据库
    cursor = conn.cursor()
    cursor.execute('select c_personid,c_name_chn from BIOG_MAIN where ((c_birthyear!=0 and c_deathyear!=0 and c_birthyear<907 and c_deathyear>618) or (c_birthyear=0 and c_deathyear!=0 and c_deathyear<947 and c_deathyear>618) or (c_birthyear!=0 and c_deathyear=0 and c_birthyear>578 and c_birthyear<907)) and c_by_nh_code!=0')
    person_info_list = cursor.fetchall()    #查询数据库
    #添加信息记录
    person_info_list.append([93495,'張繼'.decode('utf-8','ignore')])
    person_info_list.append([93409,'張旭'.decode('utf-8','ignore')])
    person_info_list.append([33753,'陸龜蒙'.decode('utf-8','ignore')])
    conn.close()    #关闭数据库
    return person_info_list   #返回诗人信息列表
#计算社团发现所用作者集合
def dealauthor_set(person_info_list,qtsauthor_set,qtsauthor_list):
    author_set=set()    #作者集合
    for temp in person_info_list:
        name=temp[1]
        if name in qtsauthor_set:
            if(qtsauthor_list.count(name)>=5):  #计算时，将作品数小于5的诗人排除在外
                author_set.add(name)
    return author_set    #返回作者集合
#查询诗人别名
def dealAlter_name(data_path,person_info_list,author_set):
    conn = sqlite3.connect(data_path)   #连接数据库
    cursor = conn.cursor()
    #删除特殊别名
    deleted_alter_names = {
    '李益'.decode('utf-8','ignore'): set(['李十'.decode('utf-8','ignore')]),
    '李世民'.decode('utf-8','ignore'): set(['李二'.decode('utf-8','ignore')]),
    '高駢'.decode('utf-8','ignore'): set(['千里'.decode('utf-8','ignore')]),
    '孟浩然'.decode('utf-8','ignore'): set(['浩然'.decode('utf-8','ignore')]),
    '李白'.decode('utf-8','ignore'): set(['太白'.decode('utf-8','ignore')])}
    #增加遗漏别名
    added_alter_names = {'劉禹錫'.decode('utf-8','ignore'): set(['劉二十八'.decode('utf-8','ignore')])}
    #查询别名
    alter_names_dict = defaultdict(set)
    for temp in person_info_list:
        if temp[1] in author_set:
            cursor.execute('SELECT c_alt_name_chn FROM ALTNAME_DATA WHERE c_personid=?',(temp[0],))
            alt_name_list = cursor.fetchall()
            for alt_name in alt_name_list:
                if len(alt_name[0]) > 1:    #若别称超过一个字，添加入别名词典
                    alter_names_dict[temp[1]].add(alt_name[0])  
    #删除特殊别名
    for k, v in deleted_alter_names.items():
      alter_names_dict[k] -= v
    #增加遗漏别名
    for k, v in added_alter_names.items():
      alter_names_dict[k] |= v
    conn.close()    #关闭数据库
    return alter_names_dict    #返回别名词典       
#对诗人相互间引用进行统计
def reference_relations_count(PoemList,author_set,alter_names_dict):
    reference_relations_counter = Counter()    #诗人相互间引用统计
    reference_relations_text = defaultdict(list)    #诗人相互间引用诗篇名称列表
    # 逐个作者计算
    for name in author_set:
    # 逐首诗寻找
        for tempPoem in PoemList:
            author=tempPoem.getAuthor()
            if author not in author_set:    #如果作者不在集合里 跳过
                continue
            title=tempPoem.getTitle()   #获取标题
            poem = title + ' '    #获取诗歌内容
            for line in tempPoem.getContent():
                poem+=line.decode('gbk','ignore')
            # 查找作者名，标题加正文中只要出现一次名字就计算一次
            if poem.find(name) != -1:
              reference_relations_counter[(author, name)] += 1
              reference_relations_text[(author, name)].append(title)
              continue
            # 查找别名
            alt_names = alter_names_dict[name]
            for alt_name in alt_names:
              if poem.find(alt_name) != -1:
                reference_relations_counter[(author, name)] += 1
                reference_relations_text[(author, name)].append(title)
                break            
    return (reference_relations_counter,reference_relations_text)    #返回诗人相互间引用统计及诗篇名称列表
#保存为csv文件
def write_to_csvfile(write_file_path,reference_relations_counter):
    csvfile = file(write_file_path,'wb')
    writer = csv.writer(csvfile)
    temp=["Source","Target","Weight"]   #稍后利用gephi进行分析，故在第一行加入列名
    writer.writerow(temp)
    for (refered_by, refered), count in reference_relations_counter.items():
        # 不统计自引用的count
        if refered_by == refered:
            continue
        if(count>=3):   #如果相互间引用大于等于三次，将其写入csv文件，具体数据筛选可灵活变通
            temp=[]
            temp.append(refered_by.decode('utf-8','ignore').encode('gbk','ignore'))
            temp.append(refered.decode('utf-8','ignore').encode('gbk','ignore'))
            temp.append(count)
            writer.writerow(temp)
    csvfile.close()
    
    
    
    
    
    
    
    
    