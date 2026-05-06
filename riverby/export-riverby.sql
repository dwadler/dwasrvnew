EXPORT
TO result.csv OF DEL
SELECT ID
     , SORT_NAME
     , FIRST_NAME
     , ADDR_NAME1
     , ADDR_NAME2
     , ADDR_LINE1
     , ADDR_LINE2
     , CITY
     , STATE
     , ZIP
     , e_mail
     , phone1
     , PHONE2
     , NOTES1
     , NOTES2
     , MAP_NUM
     , FIRE_NUM
     , RD_SECTION
     , purchase_date
     , rhha
     , billable
     , ARCHIVE
     , LASTUPDATE
     , UPDATEBY
from clc.rbyaddresses;
