# -*- coding: utf-8 -*-
#导入项目所需包
import sys
from dealData import read_qts,dealPersonInfo,dealAlter_name,dealauthor_set,reference_relations_count,write_to_csvfile
#主函数
def main():
    #进行编码设置
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #读取全唐诗，将诗歌存于列表，作者存于集合及列表
    PoemList,qtsauthor_set,qtsauthor_list=read_qts('data/qts_tradition.txt')
    #处理诗人信息列表
    person_info_list=dealPersonInfo('data/cbdb_sqlite.db')
    #计算社团发现所用作者集合
    author_set=dealauthor_set(person_info_list,qtsauthor_set,qtsauthor_list)
    #查询诗人别名
    alter_names_dict=dealAlter_name('data/cbdb_sqlite.db',person_info_list,author_set)
    #对诗人相互间引用进行统计
    reference_relations_counter,reference_relations_text=reference_relations_count(PoemList,author_set,alter_names_dict)
    #保存为csv文件
    write_to_csvfile('result/potery_relationship.csv',reference_relations_counter)
    print '诗歌总数',len(PoemList)
    print '全唐诗作者',len(qtsauthor_set)
    print '记录条数',len(person_info_list)
    print '最终作者集合',len(author_set)
    print 'over'
if __name__=="__main__":
    main()


