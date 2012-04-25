## 3. user/keys

Retrieve User's application-store-key key list

User's application-store-key key list

### URL

[https://api.uas.sdo.com/v1/user/{uid}/keys](https://api.uas.sdo.com/v1/users/{uid}/keys  user.keys")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
app_id              |  True      |  application id : full, application ids  
offset				|  True      |  int   |  
limit 				|  True      |  int   |  

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
				
		"limit": 3,  

        "items": [
        	    {

                    "app_id": 1,  
					
					"key": "self-stored-key",  

                    "created_date": "23 Apr 2012 18:06:00",

                },
        	    {

                    "app_id": 2,  
					
					"key": "self-stored-key",  

                    "created_date": "23 Apr 2012 18:06:00",

                },        	    {

                    "app_id": 3,  
					
					"key": "self-stored-key",  

                    "created_date": "23 Apr 2012 18:06:00",

                }
        ]
    }



