盛大统一用户档案 API

盛大统一用户档案APIs列表

**模块**
1. 用户
2. 应用

***APIs***

# Users:

## 1. users/show  

Retrieve Users Information

### URL 

[https://api.uas.sdo.com/1/users/show.json](https://api.uas.sdo.com/1/users/show.json "users.show")


### 
Request Parameters  |  Optional  |  Type  |  Description  
accessToken			|  False	 |  String|    
telNumber           |  True	     |  String|  User's Telephone Number
email 				|  True	     |  String|  User's Email

telNumber or email must be has one.


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

        "location": "Shanghai,China",

        "description": "Any Description.",

        ......
    }




## 2. users/update  

Update Users Information

### URL 

[https://api.uas.sdo.com/1/users/update.json](https://api.uas.sdo.com/1/users/update.json "users.update")


### 
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |    
userData            |  True	     |  String |  User's Data in JSON Format  
batch				|  True		 |  Boolean|  is Batch Update User's Data
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

        "location": "Shanghai,China",

        "description": "Any Description.",

        ......
    }




## 3. users/contacts  

Retrieve User's Contacts Information

### URL 

[https://api.uas.sdo.com/1/users/contacts.json](https://api.uas.sdo.com/1/users/contacts.json "users.contacts")


### 
Request Parameters  |  Optional  |  Type  |  Description  
accessToken			|  False	 |  String|    
telNumber           |  True	     |  String|  User's Telephone Number
email 				|  True	     |  String|  User's Email  
offset				|  True      |  int   |  User's Contacts offset  
count 				|  True      |  int   |  User's Contacts count you want to load  

telNumber or email must be has one.
offset is the count you retireve last.
count is contacts you retireve once.   
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

        "Contacts": [
        	{
        	
        		"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        		"name": "Tom",

        		"location": "Shanghai,China",

        		"description": "Any Description.",

        		......

        	},
        	{
        	
        		"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        		"name": "Tom",

        		"location": "Shanghai,China",

        		"description": "Any Description.",

        		......

        	},
        	{
        	
        		"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        		"name": "Tom",

        		"location": "Shanghai,China",

        		"description": "Any Description.",

        		......

        	},
        	......       	        
        ]
    }


# Contacts:

## 1. contacts/app

Retrieve contacts is used the app list

### URL 

[https://api.uas.sdo.com/1/contacts/app.json](https://api.uas.sdo.com/1/contacts/app.json "contacts.app")


### 
Request Parameters  |  Optional  |  Type  |  Description  
accessToken			|  False	 |  String|    
telNumber           |  True	     |  String|  User's Telephone Number
email 				|  True	     |  String|  User's Email  

telNumber or email must be has one.
App Id will be get from accessToken

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
		"app_id": 1,
		
		"app_name": "Application name"
		
        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",
			
			"user_id_in_app": "12345"
			
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4c",
			
			"user_id_in_app": "-1"

			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4d",
			
			"user_id_in_app": "-1"
			
			......
		},
		......
		]
	
		......
    }

## 2. contacts/status

Retrieve contacts last status Information

### URL 

[https://api.uas.sdo.com/1/contacts/app.json](https://api.uas.sdo.com/1/contacts/app.json "contacts.app")


### 
Request Parameters  |  Optional  |  Type   |  Description  
accessToken			|  False	 |  String |    
telNumber           |  True	     |  String |  User's Telephone Number
email 				|  True	     |  String |  User's Email  
global				|  True      |  Boolean|  is Global status  
appId				|  int       |  int    |  contacts's status in one app  

telNumber or email must be has one.

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
		"app_id": 1
		
		"app_name": "Application name"
		
        [{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",
			
			"app_id": 12345,
			
			"status": "I just want to say something!"
			
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4c",
			
			"app_id": 2,
			
			"status": "I just want to say something!------"
			
			......
		},{
			"uid": "87c09c8c-8b82-4e9f-a982-ec577074db4d",
			
			"app_id": 888,
			
			"status": "I just want to say something!!!!!!!!!"
			
			......
		},
		......
		]
		......
    }



[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"
