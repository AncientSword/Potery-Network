# -*- coding: utf-8 -*-
#诗歌类
class Poem:
    author = ''    #诗歌作者
    title= ''    #诗歌标题
    content = []    #诗歌内容
    #构造函数
    def __init__(self,author,title,content):  
        self.author = author
        self.title = title
        self.content = content
    #getitem函数
    def __getitem__(self, item):
        try:
            __index = self.key.index(item)
            return self.value[__index]
        except ValueError:
            raise KeyError('can not find the key')
    #返回诗歌作者     
    def getAuthor(self):
        return self.author
    #返回诗歌标题
    def getTitle(self):
        return self.title
    #返回诗歌内容
    def getContent(self):
        return self.content
    #更新诗歌内容
    def updateContent(self,content):
        self.content=content
    #输出诗歌内容
    def printPoem(self):
        print self.title,self.author
        for row in self.content:
            print row.decode('gbk','ignore')
