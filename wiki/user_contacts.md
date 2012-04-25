## 4. user/contacts

Retrieve User's Contacts Information

User's Contacts List  

### URL 

[https://api.uas.sdo.com/v1/user/{uid/}contacts](https://api.uas.sdo.com/v1/users/{uid}/contacts "users.contacts")


### Parameters  
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
fields              |  True      |  user profile type: base, full, custom fields  
offset				|  True      |  int   |  User's Contacts offset    
limit 				|  True      |  int   |  User's Contacts count you want to load  


offset is the count you retrieve last.
limit is contacts you retrieve once.

### Support Format  

JSON  

### HTTP Request Method  

GET

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

		"counts": 50,  
		
		"limit": 2,  

        "items": [
        	    {

                    "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

                    "name": "Tom",

                    "gender": "Male",

                    ......

                    ####end base Profile####

                    "blood": "O"  ,

                    "marry": "YES"  ,

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
                },
                {

                    "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

                    "name": "Tom",

                    "gender": "Male",

                    ......

                    ####end base Profile####

                    "blood": "O"  ,

                    "marry": "YES"  ,

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
                },
        	......       	        
        ]
    }

