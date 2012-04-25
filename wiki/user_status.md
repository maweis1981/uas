## 2. user/status

Retrieve User's status Information

User's status List

### URL

[https://api.uas.sdo.com/v1/user/{uid/}statues](https://api.uas.sdo.com/v1/users/{uid}/statues "users.statues")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
app_id              |  True      |  String| application id : full, application ids  
offset				|  True      |  int   |  
limit 				|  True      |  int   |  

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

		"counts": 50,  
				
		"limit": 2,  

        "statues": [
        	    {

                    "app_id": 1,

                    "status": "status in some application",

                    "created_date": "23 Apr 2012 18:06:00",

                },
        	    {

                    "app_id": 2,

                    "status": "status in second application",

                    "created_date": "23 Apr 2012 18:08:00",

                }
        ]
    }
