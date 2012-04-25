##  key

Retrieve stored-key value

Stored-key values

### URL

[https://api.uas.sdo.com/v1/key/{key}](https://api.uas.sdo.com/v1/key/{key}  key")


### Parameters
Request Parameters  |  Optional  |  Type  |  Description  
-------------|-----------|---------|--------
accessToken			|  False	 |  String|  


### Support Format

JSON

### HTTP Request Method

GET,POST
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

        "key": "stored-key",

        "values": "application self stored value in some application",

		"created_date": "23 Apr 2012 18:06:00"

  	}
    



[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"