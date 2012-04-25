## 3. user/key

Retrieve User's application-store-key value

User's application-store-key values

### URL

[https://api.uas.sdo.com/v1/user/{uid}/key/{key}](https://api.uas.sdo.com/v1/users/{uid}/key/{key}  users.key")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  
app_id              |  True      | String | application id : full, application ids  
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

		"app_id": 1

        "key": "stored-key",

        "values": "application self stored value in some application",

		"created_date": "23 Apr 2012 18:06:00"

  	}
    

