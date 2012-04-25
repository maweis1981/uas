## 5. user/applications

Retrieve User used applications account Information

User used application's account List

### URL

[https://api.uas.sdo.com/v1/user/{uid}/apps](https://api.uas.sdo.com/v1/users/{uid}/apps  "users.apps")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
offset				|  True      |  int   |    
limit 				|  True      |  int   |    


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

### Response ###


Application Account:[application_account]



JSON Example


    {

		"counts": 50,  
		
		"limit": 3,

        "items": [
        	    {
					"app_id": 1,

                    "uid": 311466,

                    "nickname": "Tom",

                    "gender": "Male",

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

                },{
					"app_id": 3,

                    "uid": 53153,

                    "nickname": "Tom",

                    "gender": "Male",

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

                },{
					"app_id": 4,

                    "uid": 12345,

                    "nickname": "Tom",

                    "gender": "Male",

                    "status":  "user's last status",

                    "last_use_date": "20 Apr, 2012",

                }
        ]
    }


[application_account]:"application_account_object.md"