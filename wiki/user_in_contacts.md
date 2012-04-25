## 6. user/in_contacts

Retrieve User's friends Information

User's friends List

### URL

[https://api.uas.sdo.com/v1/user/{uid}/in_contacts](https://api.uas.sdo.com/v1/users/{uid}/in_contacts  "users.in_contacts")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
fields              |  True      |  user profile type: base, full, fields  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load  

fields is full or fields("name,tel_number")
offset is friends list offset
limit is friends you retrieve once.
Just like "select * from friends limit offset, limit"

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

        "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        "name": "Tom",  

		"counts": 50,  
		
		"offset": 1,  
		
		"limit": 20,  
		
        "in_contacts": [
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

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

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

