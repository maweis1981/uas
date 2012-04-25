h1. 用户资料字典初稿
h2. 用户数据结构

table{border:1px solid black}.
|值类型|字段类型|字段说明|
|UID|string|用户唯一ID|
|FN|string|用户名字|
|N_FamilyName|string|姓|
|N_GivenName|string|名|
|N_AdditionalNames|string|附加名字|
|N_NamePrefix|string|名字前缀|
|N_NameSuffix|string|名字后缀|
|N_nick|string|昵称|
|BDAY|date|生日|
|LOGO|string|用户头像/logo地址|
|NOTE|string|用户备注|
|KEY|string|用户公钥|
|Sex|boolean|性别|
|Blood|string|血型|
|Marry|string|婚否|
|Sign|string|签名|
|Idcard|string|身份证号|
|Education|string|教育程度|
|TELs|object|用户电话资料|
|PHOTOs|object|用户图片资料|
|SOUNDs|object|用户声音资料|
|ADRs|object|用户地址资料|
|EMails|object|用户Email资料|
|IMs|object|用户即时通信资料|
|URLs|object|用户相关网址资料|
|Schools|object|用户相关网址资料|
|ORGs|object|用户单位信息|
|GEOs|object|用户地理信息资料|

|TEL对象|
|TEL_Type|string|电话类型(work,home,fax,mobile,car,pager,other)|
|TEL|string|电话|
|TEL_City|int|所在地城市id|
|TEL_Region|int|归属地地区/省id|
|TEL_location|string|所在地|


|PHOTO对象|
|PHOTO_Type|string|照片类型|
|PHOTO_url|string|照片地址|
|PHOTO_data|string|照片数据|


|SOUND对象|
|SOUND_Type|string|声音类型|
|SOUND_url|string|声音地址|
|SOUND_data|string|声音数据|


|ADR对象|
|ADR_Type|string|地址类型(home,work,other)|
|PostOfficeAddress|string|地址|
|ExtendedAddress|string|扩展地址|
|Street|string|街道|
|Locality|string|城市|
|Region|string|地区|
|PostalCode|string|邮编|
|Country|string|国家|


|EMail对象|
|EMail_Type|string|email类型(personal,work,other)|
|EMail|string|email地址|


|IM对象|
|IM_Type|string|即时通信方式(AIM,Gtalk,Yahoo,MSN,ICQ,Jabber,Skype,QQ)|
|IM|string|通信地址|


|URL对象|
|URL_Type|string|网址类型(home,homepage,work)|
|URL|string|url地址|


|School学校对象|
|School_Name|string|学校名称|
|School_City|string|学校所在地|
|School_Education|string|学校名称|


|ORG对象|
|ORG_company_Name|string|单位名称|
|ORG_company_Unit|string|单位部门|
|ORG_company_Unit_sub|string|小组|
|TITLE|string|头衔|
|ROLE|string|职务|
|WorkField|string|工作领域|


|GEO对象|
|Record_Date|date|记录时间|
|TZ|string|当地时区|
|GEO_lat|float|纬度|
|GEO_lng|float|经度|