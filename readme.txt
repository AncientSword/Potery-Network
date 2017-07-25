data: 保存本项目原始文件
      author_set(all).txt:用于社团发现作者集合
      qts_simple.txt:全唐诗简体版
      qts_tradition.txt:全唐诗繁体版
      testData.txt:测试数据
      cbdb_sqlite.db:CBDB数据库
result: 保存本项目运行结果
        potery_relationship(part).csv:著名诗人相互引用关系csv文件
        potery_relationship(part).gephi:著名诗人相互引用关系gephi文件
	potery_relationship(all).csv:诗人相互引用关系csv文件
        potery_relationship(all).gephi:诗人相互引用关系gephi文件
        potery_relationship.csv:诗人相互引用关系csv文件（运行生成）
screenshot: 保存本项目运行截图
            query_potery_information.png:查询诗人信息
            query_potery_alt_name.png:查询诗人别名
            potery_relationship(part).png:部分诗人社交网络gephi截图
            potery_relationship(all).png:诗人社交网络gephi截图
            community_detection.png:诗人社团发现结果gephi截图
test: 保存本项目实验文件
      langconv.py,zh_wiki.py:简繁转换所需文件
      simple_to_tradition_test.py:简繁转换实验代码
      sqlite_test.py:数据库连接实验代码
      sql_query.sql:数据库查询代码

Analyze.py:分析原始文件，建立诗人社交网络
dealData.py:对原始数据处理的代码
Poem.py:诗歌类

运行Analyze.py可获得运行结果
      
      