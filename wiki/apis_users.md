  




# General: #


## 1. lookup

lookup user id uri

### URL

[https://api.uas.sdo.com/v1/users/lookup](https://api.uas.sdo.com/v1/users/lookup "users.lookup")


### Parameters ###

Request Parameters | optional | Type | Description |
-----|:-------------------:|-------------------:|
access_token | False        | String        |  |
tel_number	|	True	| String	|	User's Telephone Number	|
email	|	True	|	String	|	User's Email


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

Just Response Base Profile  

JSON Example


    {
        count: 1,

        offset: 1,

        limit: 1,

        users:[
        {
            "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

            "tel_number": "13812345678",

            "email": "mawei02@snda.com",

            ......
        }
    }





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



## 2. user/status

Retrieve User's status Information

User's status List

### URL

[https://api.uas.sdo.com/v1/user/{uid/}statues](https://api.uas.sdo.com/v1/users/{uid}/statues "users.statues")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
app_id              |  True      |  application id : full, application ids  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load  

offset is the count you retrieve last.
limit is contacts you retrieve once.


### Support Format

JSON

### HTTP Request Method

GET,POST
C
R
U
D

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


        "statues": [
        	    {

                    "app_id": 1,

                    "status": "status in some application",

                    "created_date": "23 Apr 2012 18:06:00",

                    ......

                },
        	    {

                    "app_id": 2,

                    "status": "status in second application",

                    "created_date": "23 Apr 2012 18:08:00",

                    ......

                }
        	......
        ]
    }

## 3. user/key

Retrieve User's application-store-key value

User's application-store-key values

### URL

[https://api.uas.sdo.com/v1/user/{uid}/key/{key}](https://api.uas.sdo.com/v1/users/{uid}/key/{key}  users.key")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
app_id              |  True      |  application id : full, application ids  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load  

offset is the count you retrieve last.
limit is contacts you retrieve once.


### Support Format

JSON

### HTTP Request Method

GET,POST
C
R
U
D

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

        "key": "stored-key",

        "stored-values": [
        	    {

                    "app_id": 1,

                    "value": "application self stored value in some application",

                    "created_date": "23 Apr 2012 18:06:00",

                    ......

                },
        	    {

                    "app_id": 2,

                    "value": "application self stored value in second application",

                    "created_date": "23 Apr 2012 18:08:00",

                    ......

                }
        	......
        ]
    }





## 4. user/contacts

Retrieve User's Contacts Information

User's Contacts List  

### URL 

[https://api.uas.sdo.com/v1/user/{uid/}contacts](https://api.uas.sdo.com/v1/users/{uid}/contacts "users.contacts")


### Parameters  
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
fields              |  True      |  user profile type: base, full, fields  
offset				|  True      |  int   |  User's Contacts offset    
limit 				|  True      |  int   |  User's Contacts count you want to load  

telNumber or email must be has one.
offset is the count you retrieve last.
limit is contacts you retrieve once.
Just like "select * from contacts limit offset, limit"

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

        "Contacts": [
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



## 5. user/friends

friends is relative via backend computing.

Retrieve User's friends Information

User's friends List

### URL

[https://api.uas.sdo.com/v1/user/{uid}/friends](https://api.uas.sdo.com/v1/users/{uid}/friends  "users.friends")


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

        "Contacts": [
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



## 7. user/contacts/app

Retrieve contacts is used the app list

### URL

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}  "user.contacts.app")


### Parameters
|Request Parameters  |  Optional  |  Type  |  Description  
|accessToken			|  False	 |  String|  
|uid                    |  False     |  String|  User's id  
|app_id 			    |   False     |  String|  support full, app id array such as "1,2,3"  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load  


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
		"app_id": "full",

		"app_name": "Application name",  
		
		"counts": 50,  
		
		"offset": 1,  
		
		"limit": 20,

        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

			accounts:[

			    {
                    "app_id": 1,

			        "user_id_in_app": "12345",

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

			        ......
			    },{
                    "app_id": 9,

                  	"user_id_in_app": "1356934",

                  	"status": "user's status in application",

                  	......
                }
			]
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4c",

			accounts:[

			    {
                    "app_id": 1,

			        "user_id_in_app": "88888",

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

			        ......
			    }
			]
			......
		},
		......
		]
    }




## 8. user/contacts/app/status

Retrieve contacts last status Information

### URL

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/status](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/status  "user.contacts.app.status")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |  
uid                 |  True	     |  String |  User's id  
app_id 				|  True	     |  String |  Application id, support full,and fields "1,2,3"  
status              |  True      |  String |  if Application allow, Application could support status  features without coding.  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load   



### Support Format

JSON

### HTTP Request Method

GET,POST

CRUD

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
		"app_id": 1

		"app_name": "Application name",  
		
		"counts": 50,  
		
		"offset": 1,  
		
		"limit": 20,
		

        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

			statuses: [
			    {
			        "app_id": 12345,

			        "status": "I just want to say something!",

			        "created_date": "2012-05-01 13:13:33"
			    },{
			        "app_id": 54321,

			        "status": "Someone say something!",

			        "created_date": "2012-05-01 13:13:33"
			    }

			]
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4c",

			statuses: [
			    {
			        "app_id": 12345,

			        "status": "I just want to say something!",

			        "created_date": "2012-05-01 13:13:33"
			    }
			]

		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4d",

			statuses: [
			    {
			        "app_id": 12345,

			        "status": "I just want to say something!",

			        "created_date": "2012-05-01 13:13:33"
			    },{
			        "app_id": 54321,

			        "status": "Someone say something!",

			        "created_date": "2012-05-01 13:13:33"
			    },{
			        "app_id": 333,

			        "status": "Someone say something!",

			        "created_date": "2012-05-01 13:13:33"
			    }
			]
		},
		......
		]
		......
    }

## 9. user/contacts/app/key

Retrieve contacts last status Information

### URL

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/key/{key}](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/key/{key} "user.contacts.app.key")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |  
uid                 |  True	     |  String |  User's id  
app_id 				|  True	     |  String |  Application id, support full,and fields "1,2,3"  
key            |  False     |  String |  Application want to store meta key  
value          |  False     |  Object |  Application want to store meta value  
offset				|  True      |  int   |  User's Contacts offset  
limit 				|  True      |  int   |  User's Contacts count you want to load  

### Support Format

JSON

### HTTP Request Method

GET,POST

CRUD

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
		"app_id": 1

		"app_name": "Application name",  
		
		"counts": 50,  
		
		"offset": 1,  
		
		"limit": 20,
		

        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

			statuses: [
			    {
			        "app_id": 12345,

			        "self-stored-key": "self-stored-value for this app",

			        "created_date": "2012-05-01 13:13:33"
			    },{
			        "app_id": 54321,

			        "self-stored-key": "self-stored-value for this app",

			        "created_date": "2012-05-01 13:13:33"
			    }

			]
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4c",

			statuses: [
			    {
			        "app_id": 12345,

			        "self-stored-key": "self-stored-value for this app",

			        "created_date": "2012-05-01 13:13:33"
			    }
			]

		},
		......
		]
		......
    }




## 10. users batch update

Update Users Information

### URL

[https://api.uas.sdo.com/v1/users/update](https://api.uas.sdo.com/v1/users/update  "users.update")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |  
userData            |  True	     |  String |  User's Data in JSON Format  
count 				|  int       |  int    |  how many users you batch update .  

### Support Format

JSON

### HTTP Request Method

POST

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
    }



#Application:

	Empty Now.  



#Errors:

## 1. Uniform Error Response

### Response

JSON Example


    {
        "error":  {

            "message": "(#401) Error Message",

            "type": "Exception Type",

            "code": 401
        }
    }

Exceptions:

| --------------------------------|  
|  code  |  message    |  type  |  
|  401   |  Forbidden  |  Auth  |  
|  701   |  Over Limits|  Rates |  
...

<table>
    <tr>
        <td>Code</td>
        <td>Message</td>
        <td>Type</td>
    </tr>    
    	<tr>
            <td>401</td>
            <td>Forbidden</td>
            <td>Auth</td>
    	</tr>
        
    	<tr>
            <td>701</td>
            <td>Over Limits</td>
            <td>Rates</td>
    	</tr>
    
</table>  






[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"
