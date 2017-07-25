# -*- coding: utf-8 -*-
import sqlite3
#建立连接
conn = sqlite3.connect('D:\\study information\\Interesting Programmes\\python\\potery network\\cbdb_sqlite.db')
#进行查询
cursor = conn.cursor()
cursor.execute('select c_personid,c_name_chn from BIOG_MAIN where ((c_birthyear!=0 and c_deathyear!=0 and c_birthyear<907 and c_deathyear>618) or (c_birthyear=0 and c_deathyear!=0 and c_deathyear<947 and c_deathyear>618) or (c_birthyear!=0 and c_deathyear=0 and c_birthyear>578 and c_birthyear<907)) and c_by_nh_code!=0')
person_info_list = cursor.fetchall()
print len(person_info_list)
