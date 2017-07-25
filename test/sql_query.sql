select *
from BIOG_MAIN
where ((c_birthyear!=0 and c_deathyear!=0 and c_birthyear<907 and c_deathyear>618) or (c_birthyear=0 and c_deathyear!=0 and c_deathyear<947 and c_deathyear>618) or (c_birthyear!=0 and c_deathyear=0 and c_birthyear>578 and c_birthyear<907)) and c_by_nh_code!=0
order by c_by_nh_code desc

select *
from BIOG_MAIN
where c_name_chn='üS³²'