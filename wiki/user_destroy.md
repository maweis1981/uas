## user.destroy


### URL 

[https://api.uas.sdo.com/v1/user/{uid}/destroy](https://api.uas.sdo.com/v1/user/{uid}/destroy "user.destroy")


### Parameters      
Request Parameters  |  Optional     |  Type   |  Description       
-------------|-----------|---------|--------
|accessToken		 |  False	     |  String |                     |  
|fields              |  True         |  String |  Fields,support "base","full","field1,field2,..."  


### Support Format  

JSON  

### HTTP Request Method  

POST  : Destroy User  

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


 [user_base_object]:user_object.md "user object"
 [user_full_object]:user_object.md "user object"
 [user_custom_fields_object]:user_object.md "user object"
