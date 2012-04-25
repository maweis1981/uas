# Users:

## 1. user

user CRUD uri

### URL 

[https://api.uas.sdo.com/v1/user/{uid}](https://api.uas.sdo.com/v1/user/{uid} "user")


### Parameters      
Request Parameters  |  Optional     |  Type   |  Description       
-------------|-----------|---------|--------
|accessToken		 |  False	     |  String |                     |  
|fields              |  True         |  String |  Fields,support "base","full","field1,field2,..."  
|command             |  True         |  String |  C,R,U,D  C,D should be in GET, R,U should be in POST  


### Support Format  

JSON  

### HTTP Request Method  

GET,POST

GET   : Retrieve User, Delete User
POST  : Create or Update User

### Authorization  

YES


About Authorization [authorization][1]  

### Access Limits  

Level: General  
Rates Limits: YES  


About Rates Limits [Rates Limit][2]

### Response  

JSON Example   


    {

        "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        "name": "Tom",

        "gender": "Male",

        "status":  "user's last status",

        "last_use_date": "20 Apr, 2012",

        ......

        ####end base Profile####

        "blood": "O"  ,

        "marry": "YES"  ,  

		"applications": [
			{
				"app_id": 1,  
				
				"account_id": 12345,  
				
				"account_nickname": "maven",  
				
				"last_status": "just a status",  
				
				...   
				
			}
		],  

        tel_numbers:[
            {
                "tel_number":  "13512345678",

                "tel_type": "work",

                ......

            },{
                "tel_number":  "13588888888",

                "tel_type": "home",

                ......

            }
        ],

        avatars:[],

        ring_tones:[],

        locations:[],

        ...
    }

