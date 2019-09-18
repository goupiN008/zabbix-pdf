set CUR_YYYY=%date:~10,4%
set CUR_MM=%date:~4,2%
set CUR_DD=%date:~7,2%
set datetime=%CUR_YYYY%%CUR_MM%%CUR_DD%
wmic csproduct get name >> sn_computer%datetime%.txt
wmic bios get serialnumber >> sn_computer"%datetime%.txt"


