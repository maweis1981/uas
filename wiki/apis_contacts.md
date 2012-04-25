# Contacts:

## 1. user/contacts/app/accounts

Retrieve contacts is used the app list

### URL 

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/account](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/account  "user.contacts.app.account")


### Parameters  
|Request Parameters  |  Optional  |  Type  |  Description  
|accessToken			|  False	 |  String|    
|uid                    |  False     |  String|  User's id  
|app_id 			    |   False     |  String|  support full, app id array such as "1,2,3"


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
		
		"app_name": "Application name"
		
        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",
			
			accounts:[

			    {
                    "app_id": 1,

			        "user_id_in_app": "12345",

			        ......
			    },{
                    "app_id": 9,

                  	"user_id_in_app": "1356934",

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

			        ......
			    }
			]
			......
		},
		......
		]
    }




## 2. user/contacts/app/status

Retrieve contacts last status Information

### URL 

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/status](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/status  "user.contacts.app.status")


### Parameters  
Request Parameters  |  Optional  |  Type   |  Description   
accessToken			|  False	 |  String |     
uid                 |  True	     |  String |  User's id  
app_id 				|  True	     |  String |  Application id, support full,and fields "1,2,3"  
status              |  True      |  String |  if Application allow, Application could support status features without coding.  


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
		
		"app_name": "Application name"
		
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

## 3. user/contacts/app/meta_data

Retrieve contacts last status Information

### URL

[https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/{meta_data}](https://api.uas.sdo.com/v1/user/{uid}/contacts/app/{app_id}/{meta_data} "user.contacts.app.meta_data")


### Parameters  
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |  
uid                 |  True	     |  String |  User's id  
app_id 				|  True	     |  String |  Application id, support full,and fields "1,2,3"  
meta_key            |  False     |  String |  Application want to store meta key  
meta_value          |  False     |  Object |  Application want to store meta value  


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

		"app_name": "Application name"

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


[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"
