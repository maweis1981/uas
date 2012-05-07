# User #

-----

* User  

	** Base User Profile  
	** More User Profile  

-----  

## Base User Profile ##


Field Name   |   Type  |  Description
-------------|---------|--------------
uid|String|identify of user
family_name|String|
given_name|String|
gender|String|
birthday|Date|user birthday
marry|String|
blood|String|


## More User Profile ## 

Field Name | Type | Description  
-----------|------|-------------
uid|String|identify of user
applitions|Array|applicion object array
telphones|Array|telephone object array
emails|Array|user's email object array
address|Array|user's address object array
im|Array|user's im info object array
urls|Array|url object array
organization|Array|user org object array
education|Array|user education object array
photos|Array|user photo object array
sounds|Array|user sound object array

## extend User Profile ## 


## nick_name Object ##

Field Name | Type | Description  
-----------|------|-------------
app_id|String|
nick_name|Array|user's nickname of apps


## applition Object ##

Field Name | Type | Description  
-----------|------|-------------
app_id|String|
account_id|String|
account_nick_name|Stirng|
account_avatar|Stirng|
last_status|Stirng|


## Telephone Object ##

Field Name | Type | Description  
-----------|------|-------------
tel_type|String|  _建议注明标准和建议值_
tel_number|String|


## Email Object ##

Field Name | Type | Description  
-----------|------|-------------
email_type|String|  _建议注明标准和建议值_
email|String|


## IM Object ##

Field Name | Type | Description  
-----------|------|-------------
IM_type|String|QQ,gtalk...  _建议注明标准和建议值_
IM|String|IM account


## url Object ##

Field Name | Type | Description  
-----------|------|-------------
url_type|String|homepage,blog.....	_建议注明必须采用和建议采用的值，建议参考[HTML][html5-link-types]和[Microformats][microformats]的标准或约定_
url|String|


## Adress Object ##

Field Name | Type | Description  
-----------|------|-------------
address_type|String|work,home...
post_office_address|String| 
street|String|
locality|String|
region|String|
postal_code|String|
country|String|


## Organization Object ##

Field Name | Type | Description  
-----------|------|-------------
org_company_Name|String|
org_company_Unit|String| 
org_company_Unit_sub|String|
title|String|
role|String|
work_field|String|
org_company_logo|String|
org_into_date|Date|
org_leave_date|Date|



## Education Object ##

Field Name | Type | Description  
-----------|------|-------------
school_education|String|
school_name|String|
school_city|String| 
school_into_date|Date|
school_leave_date|Date|



## contact base info Object ##

Field Name | Type | Description  
-----------|------|-------------
uid|String|
from_app|String|
contact_uid|String|
contact_alias|String|
contact_group|String|
contact_relation|String|
contact_note|String|
contact_events|Array|contact event date array
contact_lastdate|date|



## contact event Object ##

Field Name | Type | Description  
-----------|------|-------------
event_type|String|
event_caption|String|
event_date|Date|

[html5-link-types]: http://www.whatwg.org/specs/web-apps/current-work/#linkTypes
[microformats]: http://microformats.org/wiki/existing-rel-values 
